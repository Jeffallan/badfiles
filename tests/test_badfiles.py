import pytest
from badfiles.badfiles import Badfile

# from .driver import main

# T = main()


b = Badfile()

# def test_number_violations():
#    """This test validates the correct number of errors are found"""
#    assert len(T) == 6
#


def test_find_zipslip():
    # assert str(T["zipslip.zip"][0]) == "zip_slip"
    assert b.is_badfile("test/zipslip.zip")


def test_find_gid():
    assert b.is_badfile("test/gid.zip")


def test_symlink():
    assert b.is_badfile("test/sym1.zip")


def test_uid():
    assert b.is_badfile("test/uid.zip")


@pytest.mark.skip(reason="Not Implemented")
def test_uid_sticky_with_bit():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_gid_sticky_with_bit():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_uid_gid():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_uid_gid_sticky_with_bit():
    pass


def test_flat_bomb():
    assert b.is_badfile("test/flat-bomb.zip")


def test_nested_bomb():
    assert b.is_badfile("test/nested-bomb.zip")


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
