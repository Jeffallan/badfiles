import pathlib

import pytest
from badfiles.badfiles import Badfile

# from .driver import main

# T = main()


b = Badfile()


def test_number_violations():
    """This test validates the correct number of errors are found"""
    hits = []  # 6
    for d in pathlib.Path("test").iterdir():
        if d.is_file():
            if b.is_badfile(d).classification == "unsafe":
                hits.append(b.is_badfile(d))
    print("\n", *hits, sep="\n")
    assert len(hits) == 14


def test_find_zipslip():
    assert b.is_badfile("test/zipslip.zip").classification == "unsafe"


def test_find_gid():
    assert b.is_badfile("test/gid.zip").classification == "unsafe"


def test_symlink():
    assert b.is_badfile("test/sym1.zip").classification == "unsafe"


def test_uid():
    assert b.is_badfile("test/uid.zip").classification == "unsafe"


def test_uid_with_sticky_bit():
    assert b.is_badfile("test/uid_sticky.zip").classification == "unsafe"


def test_gid_with_sticky_bit():
    assert b.is_badfile("test/gid_sticky.zip").classification == "unsafe"


def test_uid_gid():
    assert b.is_badfile("test/uid_gid.zip").classification == "unsafe"


def test_uid_gid_sticky_with_bit():
    assert b.is_badfile("test/uid_gid_sticky.zip").classification == "unsafe"


def test_flat_bomb():
    assert b.is_badfile("test/flat-bomb.zip").classification == "unsafe"


def test_nested_bomb():
    assert b.is_badfile("test/nested-bomb.zip").classification == "unsafe"


def test_mime_confusion():
    f = b.is_badfile("test/not_zip.zip")
    assert f.classification == "unsafe" and f.message == "deceptive extension"


@pytest.mark.skip(reason="Not Implemented")
def test_dde_payload():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_vba_payload():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_tar_uid_1000():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_tar_gid_1000():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_tar_absolute_file_path():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_tar_dotfile():
    pass
