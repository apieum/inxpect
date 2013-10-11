# -*- coding: utf8 -*-
__all__ = ['expect_factory']
from types import FunctionType, MethodType
from . import expect
from .expect.getters import AttrByName

def expect_factory(template, depth=1):
    attrs = {}
    for member_name in dir(template):
        member = getattr(template, member_name)
        if member_name[0] != '_' and _is_property(member):
            if use_DictMethod(member):
                attrs[member_name] = make_method(expect.DictMethod, member_name)
                attrs[item_name(member_name)] = make_method(expect.DictItemMethod, member_name)
            elif use_ListMethod(member):
                attrs[member_name] = make_method(expect.ListMethod, member_name)
                attrs[item_name(member_name)] = make_method(expect.ListItemMethod, member_name)
            elif use_DefaultMethod(member):
                attrs[member_name] = make_method(expect.DefaultMethod, member_name)
            elif isinstance(member, (object, type)):
                if depth > 0:
                    attrs[member_name] = expect_factory(member, depth-1)
                else:
                    attrs[member_name] = make_method(expect.DefaultMethod, member_name)



    name = getattr(template, '__name__', type(template).__name__)
    return type('expect_%s'% name, (object, ), attrs)

def item_name(member_name):
    if member_name.endswith('s'):
        item_name = member_name[0:-1]
    else:
        item_name = member_name + "Item"
    return item_name

def make_method(member_type, member_name):
    return member_type(AttrByName(member_name))

def use_DefaultMethod(value):
    return type(value) not in (type, object) and type(value).__module__ in ('__builtin__', 'builtins')

def use_DictMethod(value):
    return isinstance(value, dict)

def use_ListMethod(value):
    return isinstance(value, list)

_is_property = lambda member: not isinstance(member, (MethodType, FunctionType, staticmethod, classmethod))
