# -*- coding: utf-8 -*-
"""
utils file module.
"""

import subfix.utils.path as path_utils


def read_file(file_path, **options):
    """
    reads the given file and returns its content.

    note that all other optional keyword arguments of builtin
    open method, could be passed through options keyword arguments.
    the only exception is `mode` which will always be prefixed with `r`.

    :param str file_path: file path to read it.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises FileNotExistedError: file not existed error.

    :rtype: bytes | str
    """

    path_utils.assert_file_exists(file_path)
    mode = options.get('mode', None)
    if mode is not None and 'r' not in mode:
        mode = 'r{mode}'.format(mode=mode)
        options.update(mode=mode)
    return open(file_path, **options).read()


def read_file_bytes(file_path, **options):
    """
    reads the given file and returns its content as bytes.

    note that all other optional keyword arguments of builtin
    open method, could be passed through options keyword arguments.
    the only exception is `mode` which will always be set to `rb`.

    :param str file_path: file path to read it.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises FileNotExistedError: file not existed error.

    :rtype: bytes | str
    """

    options.update(mode='rb')
    return read_file(file_path, **options)


def open_file(file_path, **options):
    """
    opens the given file and returns its content.

    note that all other optional keyword arguments of builtin
    open method, could be passed through options keyword arguments.

    :param str file_path: file path to open.

    :keyword bool assert_exists: specifies that if the file does not
                                 exist, it should raise an error.
                                 defaults to False if not provided.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises FileNotExistedError: file not existed error.

    :rtype: IO
    """

    assert_exists = options.pop('assert_exists', False)
    if assert_exists is True:
        path_utils.assert_file_exists(file_path)

    with open(file_path, **options) as raw_file:
        return raw_file
