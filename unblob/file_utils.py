import io
import math
import os


def snull(content: bytes):
    """Strip null bytes from the end of the string."""
    return content.rstrip(b"\x00")


def round_up(size: int, alignment: int):
    """Round up size to the alignment boundary."""
    return alignment * math.ceil(size / alignment)


def find_first(file: io.BufferedIOBase, pattern: bytes) -> int:
    chunk_size = 0x1000
    compensation = len(pattern) - 1
    bytes_searched = 0
    while True:
        # Prepend the padding from the last chunk, to make sure that we find the pattern, even if
        # it straddles the chunk boundary.
        data = file.read(chunk_size)
        if data == b"":
            # We've reached the end of the stream.
            return -1
        marker = data.find(pattern)
        if marker != -1:
            return marker + bytes_searched
        file.seek(-compensation, os.SEEK_CUR)
        bytes_searched += chunk_size - compensation


class LimitedStartReader(io.BufferedIOBase):
    """Wrapper for open files, which
    enforces that seekeng earlier than the start offset is not possible.
    """

    def __init__(self, file: io.BufferedIOBase, start: int):
        self._file = file
        self._start = start
        self._file.seek(start)

    def seek(self, offset: int, whence=io.SEEK_SET):
        new_pos = self._file.seek(offset, whence)
        if new_pos < self._start:
            new_pos = self._file.seek(self._start, io.SEEK_SET)
        return new_pos

    def write(self, *args, **kwargs):
        raise TypeError("MUST NOT call write method")

    def detach(self, *args, **kwargs):
        return self._file.detach(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self._file.read(*args, **kwargs)

    def read1(self, *args, **kwargs):
        return self._file.read1(*args, **kwargs)

    def readinto(self, *args, **kwargs):
        return self._file.readinto(*args, **kwargs)

    def readinto1(self, *args, **kwargs):
        return self._file.readinto1(*args, **kwargs)
