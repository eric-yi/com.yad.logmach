#!/usr/bin/env python
# -*- coding:utf-8 -*-

from re import *
import json
from numpy import *

def fetch(filename):
    _file = open(filename, 'r')
    _feature_list = []
    for _line in _file:
        _json_str = json.loads(_line)
        _feature_list.append(_json_str)

    keys_list = []
    key_statistics_dic = {}
    for _feature in _feature_list:
        keys = []
        for (k, v) in _feature.items():
            keys.append(k)
            if k in key_statistics_dic:
                key_statistics_dic[k] += 1
            else:
                key_statistics_dic[k] = 1
        keys_list.append(keys)

    _statistics_max = 0
    _statistics_min = 0
    for (k, v) in key_statistics_dic.items():
        #print '%s= %d, ' % (k, v)
        if v > _statistics_max:
            _statistics_max = v
        if v < _statistics_min or _statistics_min == 0:
            _statistics_min = v

    _range = _statistics_max -  _statistics_min
    #print 'max= %d, min = %d' % (_statistics_max, _statistics_min)
    _feature_rate = {}
    for (k, v) in key_statistics_dic.items():
        _rate = (v - _statistics_min) / float (_range)
        _feature_rate[k] = _rate
        #print '%s= %f, ' % (k, _feature_rate[k])

    p1_num, p0_num = training_keys(keys_list, _feature_rate)
    _p1_total = sum(p1_num)
    _p0_total = sum(p0_num)
    _total = _p1_total + _p0_total
    #print 'total is %d' % (_total)

    _p1_rate = _p1_total / float(_total)
    _p0_rate = _p0_total / float(_total)

    _doc_num = len(keys_list)
    _rate_p1 = []
    _rate_p0 = []
    for i in range(_doc_num):
        _p1 = p1_num[i]
        _p0 = p0_num[i]
        p1_rate = _p1 / (_p1 + _p0) * _p1_rate / ((_p1 + _p0) / _total)
        p0_rate = _p0 / (_p1 + _p0) * _p0_rate / ((_p1 + _p0) / _total)
        _rate_p1.append(p1_rate)
        _rate_p0.append(p0_rate)
        #print '%d line: positive rate= %f, negative rate= %f' % (i, p1_rate, p0_rate)

    for i in range(_doc_num):
        p1_rate = _rate_p1[i] / sum(_rate_p1)
        p0_rate = _rate_p0[i] / sum(_rate_p0)
        clazz = 'one'
        if p1_rate < p0_rate:
            clazz = 'two'
        print '%d line: positive= %f, negative= %f, %s' % (i, p1_rate, p0_rate, clazz)



def training_keys(keys_list, key_rate):
    _doc_num = len(keys_list)
    p0_num = zeros(_doc_num)
    p1_num = zeros(_doc_num)
    i = 0
    for keys in keys_list:
        for key in keys:
            _rate = key_rate[key]
            if _rate >= 0.5:
                p1_num[i] += 1
            else:
                p0_num[i] += 1
        i += 1

    #for i in range(_doc_num):
    #    print '%d line: positive = %d, negative = %d' % (i, p1_num[i], p0_num[i])

    return p1_num, p0_num


def fetch_temp(filename):
    _file = open(filename, 'r')
    _logs = []
    _log_items = []
    _date_pattern = '^\[\d{1,2}/\d{1,2}/\d{2}'
    for _line in _file:
        if len(_line.strip()) > 0:
            merge_by_date(_date_pattern, _line, _line, _logs, _log_items)
    if len(_log_items) > 0:
        _logs.append(_log_items)

    _patterns = [
        '\[\d{1,2}/\d{1,2}/\d{2}\s\d{1,2}:\d{2}:\d{2}:\d{3}\s\S*\]\s+',
        '\w+\s+',
        '\S+\s+',
        '\S+\s+'
    ]

    _new_logs = []
    for _log in _logs:
        _log_str = ''.join(_log)
        _items = split_log(_patterns, _log_str)
        _new_logs.append(_items)

    #print_log(_new_logs)

    _date_pattern = '^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}'
    _log_items = []
    _logs = []
    for _log in _new_logs:
        _message = _log[-1]
        #print _message
        merge_by_date(_date_pattern, _message, _log, _logs, _log_items)
    if len(_log_items) > 0:
        _logs.append(_log_items)

    print_log(_logs)

    for _log in _logs:
        for _items in _log:
            for _item in _items:
                if '请求参数明文：' in _item:
                    print _item.split('请求参数明文：')[-1].split('\n')[0]



def print_log(logs):
    for log in logs:
        for item in log:
            print item
        print '=============='

def merge_by_date(date_pattern, message, log, logs, items):
    pattern = compile(date_pattern)
    if (pattern.match(message)):
        if len(items) > 0:
            logs.append(items)
            items = []
    items.append(log)

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
