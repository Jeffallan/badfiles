import pytest

from .driver import main

T = main()


def test_number_violations():
    """This test validates the correct number of errors are found"""
    assert len(T) == 6


def test_find_zipslip():
    assert str(T["zipslip.zip"][0]) == "zip_slip"


def test_find_gid():
    assert str(T["gid.zip"][0]) == "zip_setgid"


def test_symlink():
    assert str(T["sym1.zip"][0]) == "zip_symlink"


def test_uid():
    assert str(T["uid.zip"][0]) == "zip_setuid"


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
    assert str(T["flat-bomb.zip"]) == "flat_zip_bomb"


def test_nested_bomb():
    assert str(T["nested-bomb.zip"][0]) == "nested_zip_bomb"


def test_false_positives_when_searching_zip_string():
    """Make sure we only search for the string .zip in .zip files"""
    assert "not_zip.txt" not in T


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
