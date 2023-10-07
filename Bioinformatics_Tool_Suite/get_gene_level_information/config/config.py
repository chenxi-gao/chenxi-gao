"""
This Module is used for configuration
"""
# Error" doesn't conform to snake_case naming style
# pylint: disable=invalid-name

_DIRECTORY_FOR_UNIGENE = "test_database"
_FILE_ENDING_FOR_UNIGENE = "unigene"


def get_directory_for_unigene() -> str:
    """
    return the variable _DIRECTORY_FOR_UNIGENE that will be found in config.config.py
    """
    return _DIRECTORY_FOR_UNIGENE


def get_extension_for_unigene() -> str:
    """
    return the variable _FILE_ENDING_FOR_UNIGENE that we defined in config.config.py
    """
    return _FILE_ENDING_FOR_UNIGENE


def get_keywords_for_hosts() -> dict:
    """
    return a dictionary of the hosts that will be found in config.config.py module.
    """
    bos_tarus = "Bos_taurus"
    equus_caballus = "Equus_caballus"
    homo_sapiens = "Homo_sapiens"
    mus_musculus = "Mus_musculus"
    ovis_aries = "Ovis_aries"
    rattus_norvegicus = "Rattus_norvegicus"

    host_keywords = {
        "bos taurus": bos_tarus,
        "cow": bos_tarus,
        "cows": bos_tarus,
        "equus caballus": equus_caballus,
        "homo sapiens": homo_sapiens,
        "horse": equus_caballus,
        "horses": equus_caballus,
        "human": homo_sapiens,
        "humans": homo_sapiens,
        "mice": mus_musculus,
        "mouse": mus_musculus,
        "mus musculus": mus_musculus,
        "ovis aries": ovis_aries,
        "rat": rattus_norvegicus,
        "rats": rattus_norvegicus,
        "rattus norvegicus": rattus_norvegicus,
        "sheep": ovis_aries,
        "sheeps": ovis_aries
    }
    return host_keywords


def get_error_string_4_ValueError() -> None:  # error when used get_filehandle(fh_in, "1234")
    """
    Print the invalid argument message for ValueError
    """
    print("Invalid argument Value for opening a fh_in for reading/writing")


def get_error_string_4_TypeError() -> None:  # error when used get_filehandle(fh_in, "r", "w")
    """
    Print the invalid argument message for TypeError
    """
    print("Invalid argument Type passed in:")


def get_error_string_4_opening_file_OSError(file: str, mode: str) -> None:
    """
    Print the invalid argument message for OSError
    @param file: The fh_in name
    @param mode: The mode to open the fh_in
    """
    print(f"Could not open the fh_in (os error): {file} with mode {mode}")
