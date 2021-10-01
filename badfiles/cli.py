"""Console script for badfiles."""

import pathlib

import fire  # type: ignore
from badfiles.badfiles import Badfile, isolate_or_clear
from gooey import Gooey, GooeyParser  # type: ignore


def help():
    print("badfiles")
    print("=" * len("badfiles"))
    print("A malicious file detection engine written with Python and Yara.")


@Gooey
def main():
    parser = GooeyParser(description="Badfiles")

    parser.add_argument(
        "--file", widget="FileChooser", default=None, help="A file to analyze", required=False
    )
    parser.add_argument(
        "--dir", widget="DirChooser", default=None, help="A directory to analyze", required=False
    )
    parser.add_argument(
        "--quarantine",
        widget="DirChooser",
        default=None,
        help="The directory to store files that fail the badfile test.",
        required=False,
    )
    parser.add_argument(
        "--zip_rules",
        widget="FileChooser",
        help="Path to zipfile rules.",
        default="./rules/ziprules.yara",
        required=False,
    )
    parser.add_argument(
        "--tar_rules",
        widget="FileChooser",
        help="Path to tarfile rules",
        default="./rules/tartules.yara",
        required=False,
    )
    # parser.add_argument("--gzip_rules",
    #                     widget="FileChooser",
    #                     help="Path to gzip file rules",
    #                     default=None,
    #                     required=False)
    # parser.add_argument("--image_rules",
    #                     widget="FileChooser",
    #                     help="Path to tarfile rules",
    #                     default=None,
    #                     required=False)
    # parser.add_argument("--iso_dir",
    #                     widget="FileChooser",
    #                     help="The directory to isolate badfiles",
    #                     default="./test/bad",
    #                     required=False)
    # parser.add_argument("--safe_dir",
    #                     widget="FileChooser",
    #                     help="The directory to store cleared files",
    #                     default="./test/safe",
    #                     required=False)
    #
    args = parser.parse_args()

    bad = Badfile(
        zip_rules=args.zip_rules,
        tar_rules=args.tar_rules,
        # gzip_rules=args.gzip_rules,
        # image_rules=args.image_rules
    )

    if args.file and args.dir:
        raise ValueError("Analyzing both a single file and a directory is not supported.")

    if not args.file and not args.dir:
        raise ValueError("Naming either a single file or directory is required.")

    if args.file:
        f = bad.is_badfile(args.file)
        print(f)
        isolate_or_clear(args.file, f, iso_dir=args.iso_dir, safe_dir=args.safe_dir)
        return f.message

    if args.dir:
        res = []
        for d in pathlib.Path(args.dir).iterdir():
            try:
                f = bad.is_badfile(d)
                print(f)
                isolate_or_clear(d, f, iso_dir=args.iso_dir, safe_dir=args.safe_dir)
                res.append(d)
            except IsADirectoryError:
                print(f"{d} is a directory skipping.")
                pass
        return res.message


if __name__ == "__main__":
    main()  # pragma: no cover
