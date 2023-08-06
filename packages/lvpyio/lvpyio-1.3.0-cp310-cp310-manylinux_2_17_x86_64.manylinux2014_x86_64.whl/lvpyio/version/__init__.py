#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from os import path


def _read_local_one_line_txt(file_name: str) -> str:

    self_directory = path.dirname(path.abspath(__file__))

    with open(path.join(self_directory, file_name)) as f:
        return f.read().strip()


def _get_library_version():
    """
    Get internal version of low level libraries, might be needed for user support
    """
    return _read_local_one_line_txt("dll_version.txt")


def _get_version():
    """
    Get the official version of the package
    """
    return _read_local_one_line_txt("version.txt")


__version__ = _get_version()
