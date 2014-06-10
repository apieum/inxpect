#-*- coding: utf8 -*-
import jsonpickle
try:
    jsonpickle.set_preferred_backend('yajl')
except AssertionError:
    pass


def dumps(data):
    return jsonpickle.encode(data)
def loads(data):
    return jsonpickle.decode(data)
