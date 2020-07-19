# -*- coding: utf-8 -*-
"""
converter manager module.
"""

import os.path

import chardet

import subfix.utils.file as file_utils
import subfix.utils.string as string_utils
import subfix.utils.path as path_utils

from subfix.converter.enumerations import EncodingEnum
from subfix.core.exceptions import SubfixException
from subfix.core.structs import Manager
from subfix.utils.exceptions import FileAlreadyExistedError
from subfix.converter.exceptions import InvalidSourceDirectoryError, EncodingError, \
    InvalidTargetDirectoryError, TargetDirectoryIsNotEmptyError, BatchConvertError


class ConverterManager(Manager):
    """
    converter manager class.
    """

    CONFIDENCE_THRESHOLD = 0.7
    FALLBACK_ENCODING = EncodingEnum.CP1256
    DEFAULT_ENCODING = EncodingEnum.UTF8
    DEFAULT_SLUG_LENGTH = 3
    SUBTITLE_EXTENSIONS = ['srt']

    def try_detect_encoding(self, file_path, **options):
        """
        tries to detect the encoding of given file.

        it returns the encoding and the confidence value for detected
        encoding. confidence could be from 0.0 to 1.0 based on input file.
        if it fails to detect any encoding, it returns None as encoding.

        :param str file_path: file path to detect its encoding.

        :raises InvalidPathError: invalid path error.
        :raises PathIsNotAbsoluteError: path is not absolute error.
        :raises FileNotExistedError: file not existed error.

        :returns: tuple[str encoding, float confidence]
        :rtype: tuple[str, float]
        """

        raw_bytes = file_utils.read_file_bytes(file_path)
        result = chardet.detect(raw_bytes)
        return result.get('encoding'), result.get('confidence')

    def get_encoding(self, file_path, **options):
        """
        gets the encoding of given file.

        it maps the encoding to best possible value if it could not detect it firmly.

        :param str file_path: file path to detect its encoding.

        :raises InvalidPathError: invalid path error.
        :raises PathIsNotAbsoluteError: path is not absolute error.
        :raises FileNotExistedError: file not existed error.

        :rtype: str
        """

        encoding, confidence = self.try_detect_encoding(file_path, **options)
        if encoding is not None:
            if ('utf8' in encoding.lower() or
                    'utf-8' in encoding.lower()) and \
                    confidence >= self.CONFIDENCE_THRESHOLD:
                return EncodingEnum.UTF8

            if confidence >= self.CONFIDENCE_THRESHOLD:
                return encoding

        return self.FALLBACK_ENCODING

    def convert(self, file_path, **options):
        """
        converts the encoding of given file and saves it to a new file.

        :param str file_path: file path to convert its encoding.

        :keyword str target_directory: directory to save converted file in it.
                                       defaults to the directory of the source
                                       file if not provided.

        :keyword str target_file: file name to save the converted file with it.
                                  defaults to source file name if not provided.

        :keyword str suffix: a string to be appended to target file name.
                             it will be appended at the end of file name
                             and before file extension.

        :keyword str from_encoding: the current encoding of file.
                                    if not provided, it will detect
                                    encoding on its own.

        :keyword str to_encoding: the encoding of file after conversion.
                                  defaults to `utf-8` if not provided.

        :keyword int slug_length: slug length to be appended to file name
                                  if another file with the same name existed.
                                  if not provided, an error will be raised on
                                  duplicate file name.

        :raises InvalidPathError: invalid path error.
        :raises PathIsNotAbsoluteError: path is not absolute error.
        :raises FileNotExistedError: file not existed error.
        """

        path_utils.assert_file_exists(file_path)
        target_path = self._generate_target_path(file_path, **options)
        target_directory = os.path.dirname(target_path)
        if not os.path.exists(target_directory):
            os.makedirs(target_directory, exist_ok=True)

        from_encoding = options.get('from_encoding', None)
        to_encoding = options.get('to_encoding', None)
        if from_encoding is None:
            from_encoding = self.get_encoding(file_path)
        if to_encoding is None:
            to_encoding = self.DEFAULT_ENCODING

        raw_file = file_utils.read_file(file_path, encoding=from_encoding)
        with open(target_path, 'w', encoding=to_encoding) as converted:
            converted.write(raw_file)

    def batch_convert(self, source_directory, **options):
        """
        converts all files in source directory and saves them in target directory.

        if target directory is not provided, each file will be saved next to original file.

        :param str source_directory: source directory to convert its files.
                                     all files will be discovered recursively.

        :keyword str target_directory: target directory to save converted files to.
                                       if not provided, each file will be saved
                                       next to original file. when provided, sequence
                                       naming will be applied to file names.

        :keyword str from_encoding: the current encoding of files.
                                    if not provided, it will detect
                                    encoding on its own. it's better not to
                                    provide this option to let subfix detect
                                    each file separately.

        :keyword str to_encoding: the encoding of files after conversion.
                                  defaults to utf-8 if not provided.

        :keyword str fixed_name: a fixed name to use for all files.
                                 this will apply sequence naming to file names.
                                 defaults to original file name if not provided.

        :keyword bool sequence_naming: specifies that converted file names
                                       must be suffixed with a sequence number.
                                       defaults to False if not provided.
                                       when target directory or fixed name are
                                       provided, sequence naming will be
                                       applied automatically even if this
                                       option is not set.

        :keyword str suffix: a string to be appended to target file name.
                             it will be appended at the end of file name
                             and before file extension.

        :keyword int slug_length: slug length to be appended to file name
                                  if another file with the same name existed.
                                  if not provided and sequence naming is not
                                  True, defaults to `3`. it could be set to
                                  `0` to prevent slug generation.

        :keyword list[str] extensions: extensions to be considered as subtitle.
                                       if not provided, defaults to [`srt`].

        :keyword bool silent: specifies that if each one of files
                              encountered an error on encoding, do not
                              raise error and continue with other files.
                              defaults to True if not provided.

        :raises InvalidSourceDirectoryError: invalid source directory error.
        :raises TargetDirectoryIsNotEmptyError: target directory is not empty error.
        :raises InvalidTargetDirectoryError: invalid target directory error.
        :raises FileNotExistedError: file not existed error.
        :raises FileAlreadyExistedError: file already existed error.
        :raises EncodingError: encoding error.

        :returns: list of subtitle files which has been failed to encode.
        :rtype: list[str]
        """

        if not os.path.isdir(source_directory):
            raise InvalidSourceDirectoryError('Source directory must be an existing path.')

        source_directory = os.path.abspath(source_directory)
        target_directory = options.get('target_directory')
        has_target = target_directory not in (None, '')
        if has_target:
            target_directory = os.path.abspath(target_directory)

        if has_target and target_directory.startswith(source_directory) and \
                self._contains_files(target_directory) is True:
            raise TargetDirectoryIsNotEmptyError('The provided target directory [{target}] '
                                                 'is resided in the source directory '
                                                 '[{root}] but it contains some files.'
                                            .format(target=target_directory,
                                                    root=source_directory))

        if has_target and os.path.isfile(target_directory):
            raise InvalidTargetDirectoryError('Provided target directory '
                                              '[{directory}] is a file.'
                                              .format(directory=target_directory))

        options.update(target_directory=target_directory)

        suffix = options.pop('suffix', None)
        if suffix is None:
            suffix = ''

        sequence_naming = options.get('sequence_naming', None)
        if sequence_naming is None:
            sequence_naming = False

        slug_length = options.get('slug_length', None)
        if slug_length is None and sequence_naming is not True:
            options.update(slug_length=self.DEFAULT_SLUG_LENGTH)

        fixed_name = options.get('fixed_name', None)
        if fixed_name not in (None, '') or has_target:
            sequence_naming = True

        silent = options.get('silent', True)
        failed_subtitles = dict()
        subtitles = self._discover_subtitles(source_directory,
                                             extensions=options.get('extensions'))
        for sequence, subtitle in enumerate(subtitles, start=1):
            if sequence_naming is True:
                updated_suffix = self._concat(str(sequence), suffix)
                options.update(suffix=updated_suffix)

            try:
                self.convert(subtitle, target_file=fixed_name, **options)
            except SubfixException as error:
                if silent is not True:
                    raise
                failed_subtitles[subtitle] = str(error)
                continue
            except Exception as error:
                if silent is not True:
                    raise EncodingError('Encoding error occurred on file [{sub}].'
                                        'error message: [{error}]'
                                        .format(sub=subtitle, error=error))
                failed_subtitles[subtitle] = str(error)
                continue

        if len(failed_subtitles) > 0:
            raise BatchConvertError('[{num}] subtitle files failed to convert.'
                                    .format(num=len(failed_subtitles)),
                                    data=failed_subtitles)

    def _discover_subtitles(self, source_directory, extensions=None, **options):
        """
        discovers all subtitle files in given path.

        :param str source_directory: source directory to search for subtitles.

        :param list[str] extensions: extensions to be considered as subtitle.
                                     if not provided, defaults to [`srt`].

        :raises InvalidPathError: invalid path error.
        :raises PathIsNotAbsoluteError: path is not absolute error.
        :raises DirectoryNotExistedError: directory not existed error.

        :rtype: list[str]
        """

        path_utils.assert_directory_exists(source_directory)
        subtitles = []
        for root, directories, file_names in os.walk(source_directory, followlinks=True):
            for single_file in file_names:
                file_path = os.path.join(root, single_file)
                if self._is_subtitle(file_path, extensions):
                    subtitles.append(os.path.abspath(file_path))

        return list(set(subtitles))

    def _is_subtitle(self, file_name, extensions=None):
        """
        gets a value indication that given file name is a subtitle file.

        :param str file_name: file name to be checked.

        :param list[str] extensions: extensions to be considered as subtitle.
                                     if not provided, defaults to [`srt`].

        :rtype: bool
        """

        if extensions is None or len(extensions) <= 0:
            extensions = list(self.SUBTITLE_EXTENSIONS)

        extensions = tuple(item.lower() for item in extensions)
        return file_name.lower().endswith(extensions)

    def _contains_files(self, directory):
        """
        gets a value indicating that given directory contains any files.

        :param str directory: directory to be checked.

        :rtype: bool
        """

        if not os.path.isdir(directory):
            return False

        directory = os.path.abspath(directory)
        contents = os.listdir(directory)
        for item in contents:
            file = os.path.join(directory, item)
            if os.path.isfile(file) is True:
                return True

        return False

    def _generate_target_path(self, file_path, **options):
        """
        generates the target file path based on given inputs.

        :param str file_path: file path to convert its encoding.

        :keyword str target_directory: directory to save converted file in it.
                                       defaults to the directory of the source
                                       file if not provided.

        :keyword str target_file: file name to save the converted file with it.
                                  defaults to source file name if not provided.
                                  note that the extension will be get from source
                                  file.

        :keyword str suffix: a string to be appended to target file name.
                             it will be appended at the end of file name
                             and before file extension.

        :keyword int slug_length: slug length to be appended to file name
                                  if another file with the same name existed.
                                  if not provided, an error will be raised on
                                  duplicate file name.

        :raises InvalidPathError: invalid path error.
        :raises PathIsNotAbsoluteError: path is not absolute error.
        :raises FileNotExistedError: file not existed error.
        :raises FileAlreadyExistedError: file already existed error.

        :rtype: str
        """

        file_path = file_path.rstrip('/').rstrip('\\')
        path_utils.assert_absolute(file_path)

        target_directory = options.get('target_directory', None)
        target_file = options.get('target_file', None)
        if target_file is None:
            target_file = ''
        target_file = path_utils.normalize_file_name(target_file)

        suffix = options.get('suffix', None)
        if suffix is None:
            suffix = ''

        if target_directory is not None:
            target_directory = target_directory.rstrip('/').rstrip('\\')
            path_utils.assert_absolute(target_directory)

        slug_length = options.get('slug_length', None)
        if slug_length is None or slug_length < 0:
            slug_length = 0
        slug = string_utils.generate_slug(slug_length)

        destination_dir, destination_name, extension = self._extract_name(file_path)
        if target_directory not in (None, ''):
            destination_dir = target_directory

        if target_file not in (None, '') and not target_file.isspace():
            destination_name = target_file

        new_path = self._make_name(destination_dir, destination_name,
                                   extension, suffix=suffix)
        new_duplicate_path = self._make_name(destination_dir, destination_name,
                                             extension, slug=slug, suffix=suffix)

        if not os.path.exists(new_path):
            return new_path
        elif not os.path.exists(new_duplicate_path):
            return new_duplicate_path
        elif slug_length > 0:
            options.update(target_directory=destination_dir,
                           target_file=destination_name,
                           slug_length=slug_length + 1)
            return self._generate_target_path(file_path, **options)

        raise FileAlreadyExistedError('A file with name [{file_path}] already existed.'
                                      .format(file_path=new_path))

    def _make_name(self, directory, file_name, extension, **options):
        """
        makes a file name based on given inputs and returns it.

        :param str directory: directory path.
        :param str file_name: file name without extension.
        :param str extension: extension of the file name.

        :keyword str slug: a string to be appended to file name to prevent
                           duplicate names. it could be None
        :keyword str suffix: a string to be appended to file name.
                             it could be None.

        :rtype: str
        """

        path_utils.assert_absolute(directory)

        slug = options.get('slug')
        suffix = options.get('suffix')
        if suffix is None:
            suffix = ''
        if slug is None:
            slug = ''

        slug_length = len(slug)
        suffix_length = len(suffix)
        base = os.path.join(directory, file_name)
        base = os.path.abspath(base)
        name = '{base}.{extension}'
        if slug_length > 0 and suffix_length > 0:
            name = '{base}.{slug}.{suffix}.{extension}'
        elif slug_length > 0 >= suffix_length:
            name = '{base}.{slug}.{extension}'
        elif slug_length <= 0 < suffix_length:
            name = '{base}.{suffix}.{extension}'

        result = name.format(base=base, extension=extension,
                             slug=slug, suffix=suffix)
        return result

    def _extract_name(self, file_path):
        """
        extracts different parts of given name as tuple.

        it returns a tuple of `directory_name, file_name, extension`.
        not that if each part is not present, an empty string
        would be returned for that part.

        :param str file_path: file path to be extracted.
                              it could be a full path or just a name.

        :returns: tuple[str directory_name, str file_name, str extension]
        :rtype: tuple[str, str, str]
        """

        directory_name = os.path.dirname(file_path)
        base_name = path_utils.get_name(file_path, keep_extension=False)
        extension = path_utils.get_extension(file_path)
        return directory_name, base_name, extension

    def _concat(self, start, end):
        """
        gets a value containing start and end concatenated together with a dot.

        :param str start: value to be prepended to result.
        :param str end: value to be suffixed to result.

        :rtype: str
        """

        result = '{start}.{end}'
        has_start = start not in (None, '')
        has_end = end not in (None, '')
        if has_start and has_end:
            return result.format(start=start, end=end)
        elif has_start:
            return start
        elif has_end:
            return end

        return ''


# you should use this value to access converter manager methods.
# because accessing it using `ConverterManager()` could have a
# performance overhead as it is singleton and acquires a lock.
converter_manager = ConverterManager()
