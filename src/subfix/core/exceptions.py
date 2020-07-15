# -*- coding: utf-8 -*-
"""
core exceptions module.
"""


class CoreException(Exception):
    """
    base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreException.

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


class CoreBusinessException(CoreException):
    """
    base class for all application business exceptions.
    """
    pass


class CoreAttributeError(CoreException, AttributeError):
    """
    core attribute error.
    """
    pass


class ContextAttributeError(CoreAttributeError):
    """
    context attribute error.
    """
    pass


class CoreNotImplementedError(CoreException, NotImplementedError):
    """
    core not implemented error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreNotImplementedError.

        :keyword dict data: extra data for exception.
        """

        super().__init__('This method does not have an implementation.',
                         *args, **kwargs)


class CoreTypeError(CoreException, TypeError):
    """
    core type error.
    """
    pass


class CoreValueError(CoreException, ValueError):
    """
    core value error.
    """
    pass


class CoreKeyError(CoreException, KeyError):
    """
    core key error.
    """
    pass


class CoreAssertionError(CoreException, AssertionError):
    """
    core assertion error.
    """
    pass


class CoreNotADirectoryError(CoreException, NotADirectoryError):
    """
    core not a directory error.
    """
    pass


class CoreFileNotFoundError(CoreException, FileNotFoundError):
    """
    core file not found error.
    """
    pass


class CoreNameError(CoreException, NameError):
    """
    core name error.
    """
    pass


class InvalidHookTypeError(CoreException):
    """
    invalid hook type error.
    """
    pass
