"""Test suite for module py"""
import os
import pytest

from config.io_utils import get_filehandle, is_gene_file_valid

# ignore all "Missing function or method docstring" since this is a unit test
# pylint: disable=C0116
# ignore all "Function name "test_get_filehandle_4_OSError" doesn't conform to snake_case naming style"
# pylint: disable=C0103

FILE_2_TEST = "test.txt"
PATH_EXIST = '/Users'
PATH_NONEXIST = '/Userss'


def test_existing_get_filehandle_4_reading():
    # does it open a fh_in for reading
    # create a test fh_in
    _create_test_file(FILE_2_TEST)
    # test
    test = get_filehandle(FILE_2_TEST, "r")
    assert hasattr(test, "readline") is True, "Not able to open for reading"
    test.close()
    os.remove(FILE_2_TEST)


def test_existing_get_filehandle_4_writing():
    # does it open a fh_in for writing
    # test
    test = get_filehandle(FILE_2_TEST, "w")
    assert hasattr(test, "write") is True, "Not able to open for writing"
    test.close()
    os.remove(FILE_2_TEST)


def test_get_filehandle_4_OSError():
    # does it raise on OSError
    # this should exit
    with pytest.raises(OSError):
        get_filehandle("does_not_exist.txt", "r")


def test_get_filehandle_4_ValueError():
    # does it raise on ValueError
    # this should exit
    _create_test_file(FILE_2_TEST)
    with pytest.raises(ValueError):
        get_filehandle("does_not_exist.txt", "rrr")
    os.remove(FILE_2_TEST)


def test_get_filehandle_4_TypeError():
    # does it raise on TypeError
    # this should exit
    _create_test_file(FILE_2_TEST)
    with pytest.raises(TypeError):
        get_filehandle([], "r")
    os.remove(FILE_2_TEST)


def test_is_gene_file_valid_exist():
    # does it return True
    assert is_gene_file_valid(PATH_EXIST) is True


def test_is_gene_file_valid_nonexist():
    # does it return False
    assert is_gene_file_valid(PATH_NONEXIST) is False


def _create_test_file(file):
    # not actually run, the are just helper funnctions for the test script
    # create a test fh_in
    open(file, "w").close()
