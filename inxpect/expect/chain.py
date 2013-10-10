# -*- coding: utf8 -*-
__all__ = ['Chain']

class Chain(list):
    fail = lambda self, at, *args, **kwargs: False
    success = lambda self, *args, **kwargs: True

    def __init__(self, *args):
        list.__init__(self, args)

    def __call__(self, *args, **kwargs):
        for condition in self:
            if condition(*args, **kwargs) is False:
                return self.fail(condition, *args, **kwargs)
        return self.success(*args, **kwargs)

    def on_fail(self, callback):
        if not callable(callback):
            callback = lambda self: callback
        self.fail = type(self.on_fail)(callback, self)

    def on_success(self, callback):
        if not callable(callback):
            callback = lambda self: callback
        self.success = type(self.on_success)(callback, self)

    def __or__(self, condition):
        or_condition = lambda *args, **kwargs: self(*args, **kwargs) or condition(*args, **kwargs)
        return type(self)(or_condition)

    def __and__(self, condition):
        if isinstance(condition, list):
            self.extend(condition)
        else:
            self.append(condition)
        return self

    __ror__ = __or__
    __rand__ = __and__

