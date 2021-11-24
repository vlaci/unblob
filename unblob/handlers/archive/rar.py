import io
from typing import List, Union

import rarfile
from structlog import get_logger

from ...file_utils import LimitedStartReader
from ...models import UnknownChunk, ValidChunk

logger = get_logger()

NAME = "rar"

# https://www.rarlab.com/technote.htm
YARA_RULE = """
strings:
    $magic_v4 = { 52 61 72 21 1A 07 00 }
    $magic_v5 = { 52 61 72 21 1A 07 01 00 }
condition:
    $magic_v4 or $magic_v5
"""
YARA_MATCH_OFFSET = 0


def calculate_rar_size(file: io.BufferedReader, start_offset: int):
    rar_limited = LimitedStartReader(file, start_offset)
    rar_file = rarfile.RarFile(rar_limited)
    rar_tell = rar_file._rarfile.tell()
    # The tell points after the final byte, so the size is tell() - 1
    return rar_tell - 1


def calculate_chunk(
    file: io.BufferedIOBase, start_offset: int
) -> Union[ValidChunk, UnknownChunk]:

    rar_end_offset = calculate_rar_size(file, start_offset)

    return ValidChunk(
        start_offset=start_offset,
        end_offset=rar_end_offset,
    )


def make_extract_command(inpath: str, outdir: str) -> List[str]:
    return ["unar", inpath, "-o", outdir]
