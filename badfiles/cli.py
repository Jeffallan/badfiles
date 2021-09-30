"""Console script for badfiles."""

import fire  # type: ignore


def help():
    print("badfiles")
    print("=" * len("badfiles"))
    print("A malicious file detection engine written with Python and Yara.")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
