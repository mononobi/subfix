# -*- coding: utf-8 -*-
"""
utils exceptions module.
"""

from subfix.core.exceptions import SubfixFileNotFoundError, SubfixFileExistsError, \
    SubfixAssertionError, SubfixNotADirectoryError


class FileAlreadyExistedError(SubfixFileExistsError):
    """
    file already existed error.
    """
    pass


class FileNotExistedError(SubfixFileNotFoundError):
    """
    file not existed error.
    """
    pass


class DirectoryNotExistedError(SubfixNotADirectoryError):
    """
    directory not existed error.
    """
    pass


class InvalidPathError(SubfixAssertionError):
    """
    invalid path error.
    """
    pass


class PathIsNotAbsoluteError(SubfixAssertionError):
    """
    path is not absolute error.
    """
    pass


class PathNotExistedError(SubfixAssertionError):
    """
    path not existed error.
    """
    pass
