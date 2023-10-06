"""
This Module is used for grabing the filehandle and to see if the file exits
"""

import os
from typing import IO
from config import config


def get_filehandle(file: str, mode: str) -> IO:
    """
    filehandle : get_filehandle(infile, "r")
    Takes : 2 arguments fh_in name and mode i.e. what is needed to be done with
    this fh_in. This function opens the fh_in based on the mode passed in
    the argument and returns filehandle.
    @param file: The fh_in to open for the mode
    @param mode: They way to open the fh_in, e.g. reading, writing, etc
    @return: filehandle
    """
    try:
        fobj = open(file=file, mode=mode)
        return fobj
    except OSError:
        config.get_error_string_4_opening_file_OSError(file=file, mode=mode)
        # raising like this allows the overall application to choose whether
        # to stop running gracefully or handle the exception.
        # you could have a function you implement like log_the_error(err), and then raise
        raise
    except ValueError:  # test something like io_utils.get_filehandle("does_not_exist.txt", "rrr")
        config.get_error_string_4_ValueError()
        raise
    except TypeError:  # test something like io_utils.get_filehandle([], "r")
        config.get_error_string_4_TypeError()
        raise


def is_gene_file_valid(file_name) -> bool:
    """
    This function will check to make sure the given file name exists, \
    if it does it return True else it will return False
    """
    if_valid = bool(os.path.exists(file_name))
    return if_valid
