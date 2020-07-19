# -*- coding: utf-8 -*-
"""
core structs module.
"""

from threading import Lock
from abc import abstractmethod

from subfix.core.exceptions import SubfixNotImplementedError


class SingletonMetaBase(type):
    """
    singleton meta base class.

    this is a thread-safe implementation of singleton.
    """

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        try:
            cls._lock.acquire()
            if cls._has_instance() is False:
                instance = super().__call__(*args, **kwargs)
                cls._register_instance(instance)
        finally:
            if cls._lock.locked():
                cls._lock.release()

        return cls._get_instance()

    @abstractmethod
    def _has_instance(cls):
        """
        gets a value indicating there is a registered instance.

        :raises SubfixNotImplementedError: subfix not implemented error.

        :rtype: bool
        """

        raise SubfixNotImplementedError()

    @abstractmethod
    def _register_instance(cls, instance):
        """
        registers the given instance.

        :param object instance: instance to be registered.

        :raises SubfixNotImplementedError: subfix not implemented error.
        """

        raise SubfixNotImplementedError()

    @abstractmethod
    def _get_instance(cls):
        """
        gets the registered instance.

        :raises SubfixNotImplementedError: subfix not implemented error.

        :rtype: object
        """

        raise SubfixNotImplementedError()


class MultiSingletonMeta(SingletonMetaBase):
    """
    multi singleton meta class.

    this is a thread-safe implementation of singleton.
    this class allows a unique object per each type of descendants.

    for example: {Base -> UniqueSingletonMeta, A -> Base, B -> A}
    if some_object = Base() then always Base() != A() != B() but always Base() = some_object.
    or if some_object = A() then always Base() != A() != B() but always A() = some_object.
    """

    # a dictionary containing an instance of each type.
    # in the form of: {type: instance}
    _instances = dict()
    _lock = Lock()

    def _has_instance(cls):
        """
        gets a value indicating that there is a registered instance.

        :rtype: bool
        """

        return str(cls) in cls._instances

    def _register_instance(cls, instance):
        """
        registers the given instance.
        """

        cls._instances[str(cls)] = instance

    def _get_instance(cls):
        """
        gets the registered instance.

        :rtype: object
        """

        return cls._instances.get(str(cls))


class CoreObject(object):
    """
    core object class.

    this should be used as the base object for all application objects.
    """

    def __init__(self):
        """
        initializes an instance of CoreObject.
        """

        super().__init__()
        self.__name = None

    def __setattr__(self, name, value):
        return self._setattr(name, value)

    def __repr__(self):
        """
        gets the string representation of current object.

        :rtype: str
        """

        return str(self)

    def __str__(self):
        """
        gets the string representation of current object.

        :rtype: str
        """

        return '{module}.{name}'.format(module=self.__module__,
                                        name=self.__class__.__name__)

    def get_name(self):
        """
        gets the name of the object.

        if name is not available, returns its class name.

        :rtype: str
        """

        if self.__name is not None:
            return self.__name
        return self.get_class_name()

    def _set_name(self, name):
        """
        sets new name to current object.

        :param str name: object new name.
        """

        self.__name = name

    def get_class_name(self):
        """
        gets the object's class name.

        :rtype: str
        """

        return self.__class__.__name__

    def get_module_name(self):
        """
        gets the object's module name.

        :rtype: str
        """

        return self.__class__.__module__

    def get_doc(self):
        """
        gets the docstring of the object.

        :rtype: str
        """

        return self.__doc__

    def _setattr(self, name, value):
        """
        sets the given value to specified attribute.

        :param str name: attribute name.
        :param object value: attribute value.
        """

        return super().__setattr__(name, value)


class ManagerSingletonMeta(MultiSingletonMeta):
    """
    manager singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class Manager(CoreObject, metaclass=ManagerSingletonMeta):
    """
    base manager class.

    all application manager classes must be subclassed from this one.
    """
    pass
