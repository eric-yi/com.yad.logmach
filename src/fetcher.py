#!/usr/bin/env python
# -*- coding:utf-8 -*-

from re import *

def fetch(filename):
    _file = open(filename, 'r')
    _logs = []
    _log_item = []
    for _line in _file:
        if len(_line.strip()) > 0:
            pattern = compile('^\[\d{1,2}/\d{1,2}/\d{2}')
            if (pattern.match(_line)):
                if len(_log_item) > 0:
                    _logs.append(_log_item)
                    _log_item = []
            _log_item.append(_line)
    if len(_log_item) > 0:
        _logs.append(_log_item)

    #for _log in _logs:
    #    for _item in _log:
    #        print _item
    #    print '-------------------'

    _patterns = [
        '\[\d{1,2}/\d{1,2}/\d{2}\s\d{1,2}:\d{2}:\d{2}:\d{3}\s\S{0,}\]\s',
        '\S{0,}\s',
        '\S{0,}\s',
        '\S{0,}\s'
    ]
    for _log in _logs:
        _log_str = ''.join(_log)
        print _log_str
        _items = split_log(_patterns, _log_str)
        for _item in _items:
            print _item
        print '--------------------------'


def split_log(patterns, log):
    _result = []
    _remain_log = log
    for pattern in patterns:
        _match_log, _remain_log = split_log_item(pattern, _remain_log)
        _result.append(_match_log)
    _result.append(_remain_log)
    return _result

def split_log_item(pattern, log):
    _matcher = match(pattern, log)
    if _matcher:
        _start, _end = _matcher.span()
        _item = log[_start:_end]
        return _item, log[_end:].rstrip()
    raise Exception('not match')
