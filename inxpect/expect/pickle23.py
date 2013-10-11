#-*- coding: utf8 -*-
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

if sys.version < '3':
    def dumps(data):
        return pickle.dumps(data)
    def loads(data):
        return pickle.loads(data)
else:
    def dumps(data):
        return pickle.dumps(data, 2).decode('raw_unicode_escape')
    def loads(data):
        return pickle.loads(bytes(data, 'raw_unicode_escape'))
