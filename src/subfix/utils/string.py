# -*- coding: utf-8 -*-
"""
utils string module.
"""

import random
import string


def to_lower(value):
    """
    gets the lowercase version of input string.

    :param str value: value to be lower-cased.

    :rtype: str
    """

    return value.lower()


def to_upper(value):
    """
    gets the uppercase version of input string.

    :param str value: value to be upper-cased.

    :rtype: str
    """

    return value.upper()


def generate_slug(length=5, case_converter=to_lower):
    """
    generates a random slug with provided length.

    :param int length: slug length to be generated.
                       defaults to `5` if not provided.

    :param callable case_converter: a callable to be used as case converter
                                    for generated slug. it must accept a single
                                    argument and returns a string. defaults to
                                    `to_lower` which returns the slug in lowercase.

    :rtype: str
    """

    letters_and_digits = string.ascii_letters + string.digits
    slug = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return case_converter(slug)
