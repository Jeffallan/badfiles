"""Console script for badfiles."""

import pathlib

# import fire  # type: ignore
from gooey import Gooey, GooeyParser  # type: ignore

from badfiles.badfiles import Badfile, isolate_or_clear


@Gooey(
    program_name="Badfiles",
    program_description="A malicious file detection engine written with Python and Yara.",
    default_size=(1200, 1200),
)
def main():
    parser = GooeyParser(description="Badfiles")

    target_group = parser.add_argument_group(
        "Target", "Select either a file or directory to analyze."
    )

    target_group.add_argument(
        "--file", widget="FileChooser", default=None, help="A file to analyze", required=False
    )
    target_group.add_argument(
        "--dir", widget="DirChooser", default=None, help="A directory to analyze", required=False
    )
    disposition_group = parser.add_argument_group(
        "Disposition", "Select directories to move badfiles and safe files."
    )
    disposition_group.add_argument(
        "--iso_dir",
        widget="DirChooser",
        help="The directory to isolate badfiles.",
        default=None,
        required=False,
    )

    disposition_group.add_argument(
        "--safe_dir",
        widget="DirChooser",
        help="The directory to store cleared files",
        default=None,
        required=False,
    )

    rule_group = parser.add_argument_group("Yara Rules", "Select custom Yara rules as desired.")

    rule_group.add_argument(
        "--zip_rules",
        widget="FileChooser",
        help="Path to zipfile rules.",
        default=None,
        required=False,
    )
    rule_group.add_argument(
        "--tar_rules",
        widget="FileChooser",
        help="Path to tarfile rules",
        default=None,
        required=False,
    )
    rule_group.add_argument(
        "--csv_rules",
        widget="FileChooser",
        help="Path to tarfile rules",
        default=None,
        required=False,
    )

    args = parser.parse_args()

    bad = Badfile(
        zip_rules=args.zip_rules,
        tar_rules=args.tar_rules,
        csv_rules=args.csv_rules,
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

    if args.dir:
        for d in pathlib.Path(args.dir).glob("**/*"):
            print(f"inspecting {d}")
            if d.is_file():
                f = bad.is_badfile(d)
                print(f)
                isolate_or_clear(d, f, iso_dir=args.iso_dir, safe_dir=args.safe_dir)
            else:
                print(f"{d} is a directory skipping.")
                pass


if __name__ == "__main__":
    main()  # pragma: no cover
