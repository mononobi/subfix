# -*- coding: utf-8 -*-
"""
core exceptions module.
"""


class SubfixException(Exception):
    """
    base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of SubfixException.

        :keyword dict data: extra data for exception.
        """

        super().__init__(*args)
        self._data = kwargs.get('data', None) or {}
        self._traceback = None
        self._description = str(self)

    @property
    def data(self):
        """
        gets the error data.

        :rtype: dict
        """

        return self._data

    @property
    def traceback(self):
        """
        gets the traceback of this exception.

        :rtype: object
        """

        return self._traceback

    @property
    def description(self):
        """
        gets the error description.

        :rtype: str
        """

        return self._description


class SubfixAttributeError(SubfixException, AttributeError):
    """
    subfix attribute error.
    """
    pass


class SubfixNotImplementedError(SubfixException, NotImplementedError):
    """
    subfix not implemented error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of SubfixNotImplementedError.

        :keyword dict data: extra data for exception.
        """

        super().__init__('This method does not have an implementation.',
                         *args, **kwargs)


class SubfixTypeError(SubfixException, TypeError):
    """
    subfix type error.
    """
    pass


class SubfixValueError(SubfixException, ValueError):
    """
    subfix value error.
    """
    pass


class SubfixKeyError(SubfixException, KeyError):
    """
    subfix key error.
    """
    pass


class SubfixAssertionError(SubfixException, AssertionError):
    """
    subfix assertion error.
    """
    pass


class SubfixNotADirectoryError(SubfixException, NotADirectoryError):
    """
    subfix not a directory error.
    """
    pass


class SubfixFileNotFoundError(SubfixException, FileNotFoundError):
    """
    subfix file not found error.
    """
    pass


class SubfixNameError(SubfixException, NameError):
    """
    subfix name error.
    """
    pass


class SubfixFileExistsError(SubfixException, FileExistsError):
    """
    subfix file exists error.
    """
    pass
