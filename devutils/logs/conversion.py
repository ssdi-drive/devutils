'''
Created on 26-Aug-2016

@author: dgraja
'''

import json

__trace__prefix__ = ">>>> DEV-UTILS >>>> "


def set_trace_prefix(prefix = ">>>>"):
    global __trace_prefix__
    __trace_prefix__ = str(prefix)


def as_serializable(data):
    if hasattr(data, "keys"):
        return dict([(k, data[k]) for k in data.keys() if not str(k).startswith("_")])
    elif isinstance(data, (list, tuple, set)):
        return [as_serializable(item) for item in data]


def dump(logger, name, data, indent=4):
    logger.warn(__trace_prefix__ + "%s: %s" % (name, json.dumps(as_serializable(data), indent=indent)))


def dump_list(logger, name, data, indent=4):
    logger.warn("%s %s:" % (__trace__prefix__, name))
    count = 0
    for item in data:
        count = count + 1
        logger.warn(__trace_prefix__ + "[%d]: %s" % (count, json.dumps(as_serializable(item), indent=indent)))


if __name__ == '__main__':
    pass