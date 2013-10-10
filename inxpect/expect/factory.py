# -*- coding: utf8 -*-
from .method import DefaultMethod
from .list import ListMethod
from .dict import DictMethod

class DefaultMethodFactory(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        len_args = len(args)
        if len_args == 0:
            expect = DictMethod(*self.args, **self.kwargs)
        elif len_args > 1:
            expect = ListMethod(*self.args, **self.kwargs)
        else:
            expect = DefaultMethod(*self.args, **self.kwargs)

        return expect(*args, **kwargs)

    def at(self, key, _getter_=None):
        if isinstance(key, int):
            expect = ListMethod(*self.args, **self.kwargs)
        else:
            expect = DictMethod(*self.args, **self.kwargs)

        return expect.at(key, _getter_)

    def __getattr__(self, name):
        if name in dir(DefaultMethod):
            expect = DefaultMethod(*self.args, **self.kwargs)
        elif name in dir(ListMethod):
            expect = ListMethod(*self.args, **self.kwargs)
        elif name in dir(DictMethod):
            expect = DictMethod(*self.args, **self.kwargs)

        return getattr(expect, name)

