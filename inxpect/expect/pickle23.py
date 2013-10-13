#-*- coding: utf8 -*-
import jsonpickle

# in case simplejson is not installed demson require this
jsonpickle.set_encoder_options('demjson', encoding='UTF-8')

def dumps(data):
    return jsonpickle.encode(data)
def loads(data):
    return jsonpickle.decode(data)
