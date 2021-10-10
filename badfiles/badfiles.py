import mimetypes
import os
import pathlib
import warnings
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import IO, Dict, ItemsView, List, Optional, Tuple
from zipfile import BadZipFile, LargeZipFile, ZipFile

import magic
import yara  # type: ignore


class Classification(Enum):
    SAFE = "safe"
    UNSAFE = "unsafe"
    NOT_IMPLEMENTED = "not implemented"
    UNKNOWN = "unknown"


SAFE_MSG = "Nothing malicious was detected"

BadfileMsg = namedtuple("BadfileMsg", ["classification", "message", "file"])


@dataclass
class Badfile(object):
    zip_rules: str = "./rules/zip_rules.yara"
    tar_rules: Optional[str] = None
    # gzip_rules: Optional[str] = None
    # image_rules: Optional[str] = None

    def __post_init__(self) -> None:
        self.rules = dict()
        for k, v in self.__dataclass_fields__.items():
            self.rules[k] = yara.compile(v.default) if v.default is not None else None

    def _rule_factory(self, f: PathLike, mime: str) -> BadfileMsg:
        m = f"{mime.split('/')[1]}_rules"
        if m in self.rules.keys():
            if self.rules[m] is None:
                # warnings.warn("This mime type has not been implented.")
                return BadfileMsg(
                    Classification.NOT_IMPLEMENTED.value,
                    "This mime type has not been implented.",
                    f,
                )
            return self._rule_match(self.rules[m], f)
        else:
            # add whitelisted mimetypes here
            # warnings.warn("Unrecognized mime type.")
            return BadfileMsg(
                Classification.UNKNOWN.value, "Unrecognized mime type", pathlib.Path(f).name
            )

    def _rule_match(self, rules: yara.Rules, f: PathLike):
        hits: List = []

        def cb(data):
            # print(data, msg)
            msg = BadfileMsg(
                Classification.UNSAFE.value, data["meta"]["description"], pathlib.Path(f).name
            )
            yara.CALLBACK_ABORT
            hits.append(msg)

        rules.match(str(f), callback=cb, which_callbacks=yara.CALLBACK_MATCHES)
        if len(hits) > 0:
            return hits[0]
        return BadfileMsg(Classification.SAFE.value, SAFE_MSG, pathlib.Path(f).name)

    def _mime_type_confusion(self, f: PathLike) -> Tuple[bool, str]:
        return (
            mimetypes.guess_type(f, strict=True)[0] == magic.from_file(str(f), mime=True),
            magic.from_file(str(f), mime=True),
        )

    def is_badfile(self, f: PathLike) -> BadfileMsg:
        is_mime_confusion = self._mime_type_confusion(f)
        if is_mime_confusion[0] is False:
            return BadfileMsg(
                Classification.UNSAFE.value, "deceptive extension", pathlib.Path(f).name
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
    f: PathLike, msg: BadfileMsg, iso_dir: str, safe_dir: str, safe: List = ["safe"]
):
    try:
        pathlib.Path(iso_dir).resolve().mkdir(parents=True)
        pathlib.Path(safe_dir).resolve().mkdir(parents=True)
    except FileExistsError:
        pass
    if msg.classification in safe:
        pathlib.Path(f).rename(pathlib.Path(safe_dir).resolve() / pathlib.Path(f).name)
    else:
        pathlib.Path(f).rename(pathlib.Path(iso_dir).resolve() / pathlib.Path(f).name)
