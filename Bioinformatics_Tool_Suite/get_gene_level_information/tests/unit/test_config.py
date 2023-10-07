"""Test suite for module py"""

from config.config import get_extension_for_unigene, get_keywords_for_hosts, \
    get_error_string_4_ValueError, get_error_string_4_TypeError, \
    get_error_string_4_opening_file_OSError, get_directory_for_unigene

# ignore all "Missing function or method docstring" since this is a unit test
# pylint: disable=C0116
# ignore all "Function name "test_get_filehandle_4_OSError" doesn't conform to snake_case naming style"
# pylint: disable=C0103


def test_get_directory_for_unigene():
    '''does it get the right path'''
    path = get_directory_for_unigene()
    assert path == "test_database"


def test_get_extension_for_unigene():
    '''does it get the right extension name'''
    extension = get_extension_for_unigene()
    assert extension == "unigene"


def test_get_keywords_for_hosts():
    '''does it get the dictionary for host'''
    host_dict = get_keywords_for_hosts()
    assert hasattr(host_dict, "items") is True


def test_get_error_string_4_ValueError():
    '''does it print the right information'''
    assert get_error_string_4_ValueError() is None


def test_get_error_string_4_TypeError():
    '''does it print the right information'''
    assert get_error_string_4_TypeError() is None


def test_get_error_string_4_opening_file_OSError():
    '''does it print the right information'''
    assert get_error_string_4_opening_file_OSError("test.txt", "r") is None
