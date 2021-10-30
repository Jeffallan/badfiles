import enum
import mimetypes
import os
import pathlib
import warnings
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import IO, Dict, ItemsView, List, Optional, Tuple
from zipfile import BadZipFile, LargeZipFile, Path, ZipFile

import magic
import yara  # type: ignore

from badfiles.utils import DDE_CHECKS, PKG_DIR, find_dde, process_tar, unzip_doc  # type: ignore


class Classification(Enum):
    """The results returned by the BadFile class

    Attributes:
        SAFE (str): Nothing malicious was detected.
        UNSAFE (str): Malicious content was detected.
        NOT_IMPLEMENTED (str): The file type has not been implemented in the detection engine.
        UNKNOWN (str): The file type cannot be determined.
    """

    SAFE = "safe"
    UNSAFE = "unsafe"
    NOT_IMPLEMENTED = "not implemented"
    UNKNOWN = "unknown"


SAFE_MSG = "Nothing malicious was detected"

BadfileMsg = namedtuple("BadfileMsg", ["classification", "message", "file"])


@dataclass
class Badfile(object):
    """The class that implements the badfiles detection engine.

    Attributes:
        zip_rules (Optional[str]): The path to yara detection rules for zip files (defaults to ./rules/zip_rules.yara)
        tar_rules (Optional[str]): The path to yara detection rules for tar files (defaults to ./rules/tar_rules.yara)
        csv_rules (Optional[str]): The path to yara detection rules for tar files (defaults to ./rules/csv_rules.yara)
    """

    zip_rules: Optional[str] = str(pathlib.Path(PKG_DIR).parent / "rules/zip_rules.yara")
    tar_rules: Optional[str] = str(pathlib.Path(PKG_DIR).parent / "rules/tar_rules.yara")
    csv_rules: Optional[str] = str(pathlib.Path(PKG_DIR).parent / "rules/csv_rules.yara")
    # gzip_rules: Optional[str] = None
    # image_rules: Optional[str] = None

    def __post_init__(self) -> None:
        self.rules = dict()
        for k, v in self.__dataclass_fields__.items():  # type: ignore
            self.rules[k] = yara.compile(v.default) if v.default is not None else None

    def _rule_factory(self, f: PathLike, mime: str) -> BadfileMsg:
        m = f"{mime.split('/')[1].replace('x-', '')}_rules"
        if m in self.rules.keys():
            if self.rules[m] is None:
                # warnings.warn("This mime type has not been implented.")
                return BadfileMsg(
                    Classification.NOT_IMPLEMENTED.value,
                    "This mime type has not been implented.",
                    f,
                )
            return self._rule_match(self.rules[m], f, mime)
        else:
            # check for DDE
            if mime in DDE_CHECKS:
                match = self._rule_match(self.rules["zip_rules"], f, mime="application/zip")
                # TODO pass to dde util functions.
                if match.classification == "safe":
                    if find_dde(unzip_doc(f)):
                        return BadfileMsg(
                            Classification.UNSAFE.value,
                            "DDE detected",
                            pathlib.Path(f).name,
                        )
                return match
            return BadfileMsg(
                Classification.UNKNOWN.value, f"Unrecognized mime type {mime}", pathlib.Path(f).name
            )

    def _rule_match(self, rules: yara.Rules, f: PathLike, mime: str):
        hits: List = []

        def cb(data):
            # print(data, msg)
            msg = BadfileMsg(
                Classification.UNSAFE.value, data["meta"]["description"], pathlib.Path(f).name
            )
            yara.CALLBACK_ABORT
            hits.append(msg)

        if mime == "application/x-tar":
            for t in process_tar(f):
                rules.match(data=t, callback=cb, which_callbacks=yara.CALLBACK_MATCHES)
        else:
            rules.match(str(f), callback=cb, which_callbacks=yara.CALLBACK_MATCHES)

        if len(hits) > 0:
            return hits[0]
        return BadfileMsg(Classification.SAFE.value, SAFE_MSG, pathlib.Path(f).name)

    def _mime_type_confusion(self, f: PathLike) -> Tuple[bool, str, str]:
        return (
            mimetypes.guess_type(f, strict=True)[0].split("/")[1]  # type: ignore
            == magic.from_file(str(f), mime=True).split("/")[1],
            magic.from_file(str(f), mime=True),
            mimetypes.guess_type(f, strict=True)[0],
        )

    def is_badfile(self, f: PathLike) -> BadfileMsg:
        """This function checks for various indicators of potentially malicious content including:
            - Mime Type confusion;
            - Zip files with high compression rates and;
            - Hands f to the proper yara detection rules.

        Args:
            f (PathLike): The path of the file to be analyzed

        Returns:
            BadfileMsg: The BadfileMsg named tuple
        """
        is_mime_confusion = self._mime_type_confusion(f)
        if is_mime_confusion[0] is False:
            return BadfileMsg(
                Classification.UNSAFE.value,
                f"Deceptive extension. File extension suggests {is_mime_confusion[2]} inspection shows {is_mime_confusion[1]}",
                pathlib.Path(f).name,
            )
        if is_mime_confusion[1] == "application/zip":
            if self._high_compression(f):
                return BadfileMsg(
                    Classification.UNSAFE.value, "high compression rate", pathlib.Path(f).name
                )
        return self._rule_factory(f, is_mime_confusion[1])

    def _high_compression(self, f: PathLike, rate: float = 0.75) -> bool:
        try:
            zip_file = ZipFile(f)
        except BadZipFile:
            return False
        stats = []
        for z in zip_file.infolist():
            try:
                stats.append(1 - (z.compress_size / z.file_size))
            except ZeroDivisionError:
                return False
            except LargeZipFile:
                return True  # TODO move LargeZipFile check to another function?
        if len(stats) == 0:
            return False
        return sum(stats) / len(stats) > rate


def isolate_or_clear(
    f: PathLike,
    msg: BadfileMsg,
    iso_dir: Optional[str] = None,
    safe_dir: Optional[str] = None,
    safe: List = ["safe"],
) -> None:
    def _move_file(f: PathLike, msg: BadfileMsg, safe: List = safe) -> None:
        if msg.classification in safe:
            pathlib.Path(f).rename(pathlib.Path(safe_dir).resolve() / pathlib.Path(f).name)

        else:
            pathlib.Path(f).rename(pathlib.Path(iso_dir).resolve() / pathlib.Path(f).name)

    try:
        pathlib.Path(iso_dir).resolve().mkdir(parents=True)
        pathlib.Path(safe_dir).resolve().mkdir(parents=True)
        _move_file(f, msg)

    except FileExistsError:
        pathlib.Path(iso_dir).resolve()
        pathlib.Path(safe_dir).resolve()
        _move_file(f, msg)
    except TypeError:
        pass
