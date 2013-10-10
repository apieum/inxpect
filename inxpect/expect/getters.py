# -*- coding: utf8 -*-

class AsIs(object):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

class AtIndex(object):
    def __init__(self, index, getter):
        self.index = index
        self.getter = getter

    def __call__(self, *args, **kwargs):
        return self.getter(*args, **kwargs)[self.index]

class ObjectLen(object):
    def __init__(self, getter):
        self.getter = getter

    def __call__(self, *args, **kwargs):
        return len(self.getter(*args, **kwargs))

class AttrByName(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __call__(self, instance, default=None):
        return getattr(instance, self.attr_name, default)

class AttrTypeByName(AttrByName):
    def __call__(self, instance, default=None):
        return type(AttrByName.__call__(instance, default))

class Arguments(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args = list(self.args).extend(list(args))
        kwargs = dict(self.kwargs).update(dict(kwargs))
        return args, kwargs
