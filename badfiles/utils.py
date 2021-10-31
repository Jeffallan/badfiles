import os
import pathlib
import shutil
import zipfile
from functools import partial
from os import PathLike
from pathlib import Path
from typing import BinaryIO, Generator

RULE_DIR = os.path.dirname(os.path.abspath(__file__))

DDE_CHECKS = [
    # excel
    "application/vnd.ms-excel",  # xls xlm xla xlc xlt xlw
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",  # xlsb
    "application/vnd.ms-excel.sheet.macroEnabled.12",  # xlsm
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx,
    # word
    "application/msword" "application/vnd.ms-word.document.macroEnabled.12",  # doc  # docm
    "application/vnd.ms-word.template.macroEnabled.12",  # dotm
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
    # powerpoint
    "application/vnd.ms-powerpoint",  # ppt or pps
    "application/vnd.ms-powerpoint.presentation.macroEnabled.12",  # pptm
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # pptx
]


def process_tar(f: str, chunk: int = 512) -> Generator[bytes, None, None]:
    """A generator function that yields tar file headers.

    Args:
        f (PathLike): The path the the tar file.
        chunk (int, optional): The size of the tarfile chunks. Defaults to 512.

    Yields:
        Generator[bytes, None, None]: Tar file header(s).
    """

    with open(f, "rb") as f:
        for fh in iter(partial(f.read, chunk), b""):
            try:
                data = fh
                # size = data.decode("ascii")[124:135]
                # print(size)
                if data.decode("ascii")[257:262] == "ustar" and data[125:135].isascii():
                    yield data
            except (UnicodeDecodeError, ValueError):
                pass


def find_dde(doc_dir: Path) -> bool:
    """Iterates through doc_dir and searches for a directory called externalLinks.

    Args:
        doc_dir (PathLike): The target directory to be analyzed.

    Returns:
        bool: True if a folder called externalLinks otherwise returns False.
    """
    p = Path(doc_dir)
    dde = False
    for i in p.glob("**/*"):
        if i.name.lower() == "externallinks":
            dde = True
    shutil.rmtree(doc_dir)
    return dde


def unzip_doc(doc: PathLike, dir=pathlib.Path(RULE_DIR).parent / "./tmp_doc") -> PathLike:
    """Unzips a document to enable the find_dde function.

    Args:
        doc (PathLike): The path to the document to unzip
        dir (str, optional): The directory to unzip the document. Defaults to "./tmp_doc".

    Returns:
        PathLike: The directory of the unzipped document.
    """
    z = zipfile.ZipFile(doc)
    z.extractall(path=dir)
    return dir


# if __name__ == "__main__":
#     print(RULE_DIR)
