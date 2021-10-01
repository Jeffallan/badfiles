from pathlib import Path
from typing import IO
from zipfile import BadZipFile, ZipFile

import yara


def get_rules() -> yara.Rules:
    return yara.compile("rules/zip_rules.yara")
    """
    def get_rules(dir: str="./rules") -> yara.Rules:
    #return yara.compile(filepaths={d.name.split(".")[0]: str(d) for d in Path(dir).iterdir()})
    return {d.name.split(".")[0]: yara.compile(str(d)) for d in Path(dir).iterdir()}

    """


def high_compression(f: IO, rate: float = 0.75) -> bool:
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

    return sum(stats) / len(stats) > rate


def match_callback(data):
    # print(data)
    yara.CALLBACK_CONTINUE
    return data["rule"]


def match_rules(rules: yara.Rules, f) -> yara.Match:
    return rules.match(f, callback=match_callback, which_callbacks=yara.CALLBACK_MATCHES)  #


def main():
    rules = get_rules()
    dir = Path("./test")
    violations = {}
    for d in dir.iterdir():
        m = match_rules(rules, str(d))
        if len(m) > 0:
            violations[d.name] = m
        if high_compression(d):
            violations[d.name] = "flat_zip_bomb"
    print(violations)
    # print(len(violations))
    return violations


if __name__ == "__main__":
    main()
