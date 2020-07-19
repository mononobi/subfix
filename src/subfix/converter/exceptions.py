# -*- coding: utf-8 -*-
"""
converter exceptions module.
"""

from subfix.core.exceptions import SubfixException, SubfixNotADirectoryError


class InvalidSourceDirectoryError(SubfixNotADirectoryError):
    """
    invalid source directory error.
    """
    pass


class InvalidTargetDirectoryError(SubfixNotADirectoryError):
    """
    invalid target directory error.
    """
    pass


class SequenceNamingIsRequiredError(SubfixException):
    """
    sequence naming is required error.
    """
    pass


class EncodingError(SubfixException):
    """
    encoding error.
    """
    pass


class TargetDirectoryIsNotEmptyError(SubfixException):
    """
    target directory is not empty error.
    """
    pass


class BatchConvertError(SubfixException):
    """
    batch convert error.
    """
    pass
