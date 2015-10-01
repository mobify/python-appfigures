# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


# We are vendoring this decorator because it doesn't really make sense to add
# additional dependencies for this. Instead we borrow from Django.
class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )

    This implementation is borrowed from Django's source code:
    https://github.com/django/django
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
