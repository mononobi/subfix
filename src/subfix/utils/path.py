# -*- coding: utf-8 -*-
"""
utils path module.
"""

import os

from subfix.utils.exceptions import FileNotExistedError, InvalidPathError, \
    PathIsNotAbsoluteError, PathNotExistedError, DirectoryNotExistedError


def assert_exists(path):
    """
    asserts that given path exists on filesystem.

    it raises an error if it does not exist.

    :param str path: path to be checked for existence.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_absolute(path)
    if not os.path.exists(path):
        raise PathNotExistedError('Provided path [{path}] does not exist.'
                                  .format(path=path))


def assert_file_exists(file_path):
    """
    asserts that given file exists on filesystem.

    it raises an error if it does not exist.

    :param str file_path: file path to be checked.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises FileNotExistedError: file not existed error.
    """

    assert_absolute(file_path)
    if not os.path.isfile(file_path):
        raise FileNotExistedError('Provided file [{path}] does not exist.'
                                  .format(path=file_path))


def assert_directory_exists(directory_path):
    """
    asserts that given directory exists on filesystem.

    it raises an error if it does not exist.

    :param str directory_path: directory path to be checked.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises DirectoryNotExistedError: directory not existed error.
    """

    assert_absolute(directory_path)
    if not os.path.isdir(directory_path):
        raise DirectoryNotExistedError('Provided directory [{path}] does not exist.'
                                       .format(path=directory_path))


def assert_absolute(path):
    """
    asserts that given path is absolute.

    :param str path: path to be checked.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    """

    if path is None:
        raise InvalidPathError('Provided path could not be None.')

    if not os.path.isabs(path):
        raise PathIsNotAbsoluteError('Provided path [{path}] must be absolute.'
                                     .format(path=path))


def normalize_file_name(file_name):
    """
    normalizes given file name.

    :param str file_name: file name to be normalized.

    :rtype: str
    """

    if file_name is None:
        return file_name

    invalid_chars = {'\\', '/', '*', '<', '>', ':', '"', '|', '?'}

    for item in invalid_chars:
        file_name = file_name.replace(item, '-')

    return file_name


def get_name(file_path, keep_extension=True):
    """
    gets the file name for provided file path.

    :param str file_path: file path.
    :param bool keep_extension: specifies that it should include
                                the extension in returned name.
                                defaults to True if not provided.

    :rtype: str
    """

    file_path = file_path.rstrip('/').rstrip('\\')
    base_name = os.path.basename(file_path)

    if keep_extension is not False:
        return base_name

    parts = base_name.split('.')
    if len(parts) > 1:
        parts = parts[:-1]

    name = '.'.join(parts)
    return name


def get_extension(file_path):
    """
    gets the extension of provided file.

    :param str file_path: file path.

    :rtype: str
    """

    no_extension_name = get_name(file_path, keep_extension=False)
    base_name = os.path.basename(file_path)
    extension = base_name.replace(no_extension_name, '').lstrip('.')
    return extension
