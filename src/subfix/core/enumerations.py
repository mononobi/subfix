# -*- coding: utf-8 -*-
"""
core enumerations module.
"""

from enum import EnumMeta, Enum


class CoreEnumMeta(EnumMeta):
    """
    base enum metaclass.
    """

    def __contains__(cls, member):
        """
        gets a value indicating that given input existed in
        the enumeration values.

        this method is overridden to be able to check
        for existence with `in` keyword. for example:
        has_value = 'value' in SomeEnum

        :param int | str | CoreEnum member: value to be checked for existence.

        :rtype: bool
        """

        if isinstance(member, CoreEnum):
            return EnumMeta.__contains__(cls, member)

        return member in cls._get_values()

    def _get_values(cls):
        """
        gets a set of all enumeration values.

        :rtype: set
        """

        return set(member.value for member in cls._member_map_.values())


class CoreEnum(Enum, metaclass=CoreEnumMeta):
    """
    base enum class.
    all application enumerations must inherit from this class.
    """

    def __get__(self, instance, owner):
        """
        this method is overridden to be able to access enum
        member value without having to write `enum.member.value`.
        this causes `enum.member.name` to become unavailable.
        """

        return self.value

    @classmethod
    def values(cls):
        """
        gets a set containing all values in the enumeration.

        :rtype: set
        """

        return set(item.value for item in cls)

    @classmethod
    def contains(cls, value):
        """
        gets a value indicating that given input existed in
        the enumeration values.

        :param int | str | CoreEnum value: value to be checked for existence.

        :rtype: bool
        """

        return value in cls
