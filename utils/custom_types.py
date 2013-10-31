from collections import namedtuple

# forces and their factors
Forces = namedtuple('Forces', 'social obstacle desired lookahead')
ForceFactor = namedtuple('ForceFactor', 'social obstacle desired lookahead')


class cached_property(object):
    """
    Lazy-loading read/write property descriptor.
    Value is stored locally in descriptor object. If value is not set when
    accessed, value is computed using given function. Value can be cleared
    by calling 'del'.
    """

    def __init__(self, func):
        self._func = func
        self._values = {}
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        if obj not in self._values \
                or self._values[obj] is None:
            self._values[obj] = self._func(obj)
        return self._values[obj]

    def __set__(self, obj, value):
        self._values[obj] = value

    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]
        self._values[obj] = None