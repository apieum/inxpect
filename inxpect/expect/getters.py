#-*- coding: utf8 -*-
from . import pickle23


class _getter_(object):
    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return pickle23.dumps(self)

class AnonymousFunc(_getter_):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class AsIs(_getter_):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

class FirstArg(_getter_):
    def __call__(self, *args, **kwargs):
        return args[0]

class AtIndex(_getter_):
    def __init__(self, index, getter):
        self.index = index
        self.getter = getter

    def __call__(self, *args, **kwargs):
        return self.getter(*args, **kwargs)[self.index]


class ObjectLen(_getter_):
    def __init__(self, getter):
        self.getter = getter

    def __call__(self, *args, **kwargs):
        return len(self.getter(*args, **kwargs))

class AttrByName(_getter_):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __call__(self, instance, default=None):
        return getattr(instance, self.attr_name, default)

class AttrTypeByName(AttrByName):
    def __call__(self, instance, default=None):
        return type(AttrByName.__call__(instance, default))

class Arguments(_getter_):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args = list(self.args).extend(list(args))
        kwargs = dict(self.kwargs).update(dict(kwargs))
        return args, kwargs
