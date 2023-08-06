from decord import VideoReader, AudioReader, cpu
import numpy as np
import os
import sys
import errno

from nova_utils.db_utils import nova_types as nt
from nova_utils.ssi_utils.ssi_stream_utils import Stream
from hcai_datasets.hcai_nova_dynamic.utils.nova_string_utils import (
    merge_role_key,
)
from typing import Union
from abc import ABC, abstractmethod


class Data(ABC):
    def __init__(
        self,
        role: str = "",
        name: str = "",
        file_ext: str = "stream",
        sr: int = 0,
        data_type: nt.DataTypes = None,
        is_valid: bool = True,
        sample_data_path: str = "",
        lazy_loading: bool = False,
        n_samples_per_window: int = 1
    ):
        """

        Args:
            role ():
            name ():
            file_ext ():
            sr ():
            data_type ():
            is_valid ():
            sample_data_path ():
            lazy_loading ():
        """
        self.role = role
        self.name = name
        self.is_valid = is_valid
        self.sr = sr
        self.file_ext = file_ext
        self.lazy_loading = lazy_loading
        self.data_type = data_type

        # Set when populate_meta_info is called
        self.sample_data_shape = None
        self.np_data_type = None
        self.meta_loaded = False
        self.n_frames_per_window = n_samples_per_window

        # Set when open_file_reader is called
        self.file_path = None
        self.file_reader = None
        self.dur = sys.maxsize

        if sample_data_path:
            if not os.path.isfile(sample_data_path):
                self.meta_loaded = False
                print(
                    f"WARNING: Sample file {sample_data_path} not found. Could not initialize meta data."
                )
                # raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), sample_data_path)
            else:
                self.populate_meta_info(sample_data_path)

    def data_stream_opend(self):
        if not self.file_reader:
            print(
                "No datastream opened for {}".format(
                    merge_role_key(self.role, self.name)
                )
            )
            raise RuntimeError("Datastream not loaded")

    def get_info(self):
        if self.meta_loaded:
            if self.lazy_loading:
                return {
                    "frame_start": {"dtype": np.float32, "shape": (1)},
                    "frame_end": {"dtype": np.float32, "shape": (1)},
                    "file_path": {"dtype": np.str, "shape": (None,)},
                }
            return self.get_info_hook()
        else:
            print(
                "Meta data has not been loaded for file {}. Call get_meta_info() first.".format(
                    merge_role_key(self.role, self.name)
                )
            )

    def get_sample(self, frame_start_ms: int, frame_end_ms: int):
        """
        Returns the sample for the respective frames. If lazy loading is true, only the filepath and frame_start, frame_end will be returned.
        """

        if not self.file_reader:
            start_frame = milli_seconds_to_frame(self.sr, frame_start_ms)
            end_frame = milli_seconds_to_frame(self.sr, frame_end_ms)
            return np.zeros(self.sample_data_shape + (end_frame - start_frame, ))
        elif self.lazy_loading:
            return {
                "frame_start": frame_start_ms,
                "frame_end": frame_end_ms,
                "file_path": self.file_path,
            }
        else:
            return self.get_sample_hook(frame_start_ms, frame_end_ms)

    def open_file_reader(self, path: str):
        """
        Args:
            path ():
        Raises:
            FileNotFoundError: If path is not a file
        """
        self.file_path = path
        if not os.path.isfile(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        if not self.meta_loaded:
            self.populate_meta_info(path)
        self.open_file_reader_hook(path)

    @abstractmethod
    def get_info_hook(self):
        """
        Returns the features for this datastream to create the DatasetInfo for tensorflow
        """
        ...

    @abstractmethod
    def get_sample_hook(self, start_frame: int, end_frame: int):
        """
        Returns a data chunk from start frame to end frame
        """
        ...

    @abstractmethod
    def open_file_reader_hook(self, path: str):
        """
        Opens a filereader for the respective datastream. Sets attributes self.file_reader and self.dur
        """
        ...

    @abstractmethod
    def populate_meta_info(self, path: str):
        """
        Opens a data sample from the provided path to extract additional data that is not in the database
        """
        ...

    @abstractmethod
    def close_file_reader(self):
        """
        Closes a filereader for the respective datastream
        """
        ...


class AudioData(Data):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Overwrite default
        self.sample_data_shape = (1, )

    def get_info_hook(self):
        return merge_role_key(self.role, self.name), {
            "shape": self.sample_data_shape,
            "dtype": np.float32,
        }

    def get_sample_hook(self, frame_start_ms: int, frame_end_ms: int):
        start_frame = int(frame_start_ms * self.sr / 1000)
        end_frame = int(frame_end_ms * self.sr / 1000)
        chunk = self.file_reader.get_batch(
            list(range(start_frame, end_frame))
        ).asnumpy()
        return chunk

    def open_file_reader_hook(self, path: str):
        self.file_reader = AudioReader(path, ctx=cpu(0), mono=False)
        self.dur = self.file_reader.duration()

    def populate_meta_info(self, path: str):
        """

        Args:
            path ():
        """

        file_reader = AudioReader(path, ctx=cpu(0), mono=False)
        n_channels = file_reader.shape[0]
        self.sample_data_shape = (None, n_channels)
        self.meta_loaded = True

    def close_file_reader(self):
        return True


class VideoData(Data):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Overwrite default
        self.sample_data_shape = (480, 640, 3)


    def get_info_hook(self):
        return merge_role_key(self.role, self.name), {
            "shape": self.sample_data_shape,
            "dtype": np.float32,
        }

    def get_sample_hook(self, frame_start_ms: int, frame_end_ms: int):
        start_frame = int(frame_start_ms * self.sr / 1000)
        end_frame = int(frame_end_ms * self.sr / 1000)
        chunk = self.file_reader.get_batch(
            list(range(start_frame, end_frame))
        ).asnumpy()
        return chunk

    def open_file_reader_hook(self, path: str):
        self.file_reader = VideoReader(path, ctx=cpu(0))
        fps = self.file_reader.get_avg_fps()
        frame_count = len(self.file_reader)
        self.dur = frame_count / fps

    def populate_meta_info(self, path: str):
        file_reader = VideoReader(path)
        self.sample_data_shape = file_reader[0].shape
        self.meta_loaded = True

    def close_file_reader(self):
        return True


class StreamData(Data):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Overwrite default
        self.sample_data_shape = (1, )


    def get_info_hook(self):
        return merge_role_key(self.role, self.name), {
            "shape": self.sample_data_shape,
            "dtype": self.np_data_type,
        }

    def get_sample_hook(self, frame_start_ms: int, frame_end_ms: int):
        try:
            self.data_stream_opend()
            start_frame = milli_seconds_to_frame(self.sr, frame_start_ms)
            end_frame = milli_seconds_to_frame(self.sr, frame_end_ms)

            # rounding error
            #if start_frame == end_frame:
            #    end_frame += 1
            #elif end_frame - start_frame > 1:



            return self.file_reader.data[start_frame:end_frame]
        except RuntimeError:
            print(
                "Could not get chunk {}-{} from data stream {}".format(
                    frame_start_ms, frame_end_ms, merge_role_key(self.role, self.name)
                )
            )

    def open_file_reader_hook(self, path: str) -> bool:
        stream = Stream(path=path)
        if stream:
            self.file_reader = stream
            self.dur = stream.data.shape[0] / stream.sr
            return True
        else:
            print("Could not open Stream {}".format(str))
            return False

    def close_file_reader(self):
        return True

    def populate_meta_info(self, path: str):
        stream = Stream()
        stream.load_header(path)
        self.sample_data_shape = (stream.dim,)
        self.np_data_type = stream.dtype
        self.meta_loaded = True


##########################
# General helper functions
##########################


#def frame_to_seconds(sr: int, frame: int) -> float:
#    return frame / sr


def seconds_to_frame(sr: int, time_s: float) -> int:
    return round(time_s * sr)


def milli_seconds_to_frame(sr: int, time_ms: int) -> int:
    return seconds_to_frame(sr=sr, time_s=time_ms / 1000)



def parse_time_string_to_ms(frame: Union[str, int, float]) -> int:
    # if frame is specified milliseconds as string
    if str(frame).endswith("ms"):
        try:
            return int(frame[:-2])
        except ValueError:
            raise ValueError(
                "Invalid input format for frame in milliseconds: {}".format(frame)
            )
    # if frame is specified in seconds as string
    elif str(frame).endswith("s"):
        try:
            frame_s = float(frame[:-1])
            return int(frame_s * 1000)
        except ValueError:
            raise ValueError(
                "Invalid input format for frame in seconds: {}".format(frame)
            )
    # if type is float we assume the input will be seconds
    elif isinstance(frame, float) or "." in str(frame):
        try:
            print(
                "WARNING: Automatically inferred type for frame {} is float.".format(
                    frame
                )
            )
            return int(1000 * float(frame))
        except ValueError:
            raise ValueError("Invalid input format for frame: {}".format(frame))
    # if type is int we assume the input will be milliseconds
    elif isinstance(frame, int) or (isinstance(frame, str) and frame.isdigit()):
        try:
            print(
                "WARNING: Automatically inferred type for frame {} is int.".format(
                    frame
                )
            )
            return int(frame)
        except ValueError:
            raise ValueError("Invalid input format for frame: {}".format(frame))

    print(
        f'WARNING: Could  not automatically parse time "{frame}" to seconds. Returning None '
    )
