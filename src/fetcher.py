#!/usr/bin/env python
# -*- coding:utf-8 -*-

from re import *
import json
from numpy import *
import time

def fetch(filename):
    _file = open(filename, 'r')
    feature_list = fetch_feature_list(_file)
    keys_list, key_statistics_dic = split_feature(feature_list)
    statistics_min, statistics_max = calculate_extremum(key_statistics_dic)
    feature_rate = calculate(key_statistics_dic, statistics_min, statistics_max)
    p1_num, p0_num = training_keys(keys_list, feature_rate)
    p0_bayes, p1_bayes = training_by_bayes(keys_list, p0_num, p1_num)
    result_file = '../logs/result_%d.log' % (int(time.time()))
    write_result(result_file, len(keys_list), p0_bayes, p1_bayes)

def fetch_feature_list(_file):
    feature_list = []
    for line in _file:
        json_str = json.loads(line)
        feature_list.append(json_str)
    return feature_list

def split_feature(feature_list):
    keys_list = []
    key_statistics_dic = {}
    for feature in feature_list:
        keys = []
        for (k, v) in feature.items():
            keys.append(k)
            if k in key_statistics_dic:
                key_statistics_dic[k] += 1
            else:
                key_statistics_dic[k] = 1
        keys_list.append(keys)

    return keys_list, key_statistics_dic

def calculate_extremum(key_statistics_dic):
    statistics_max = 0
    statistics_min = 0
    for (k, v) in key_statistics_dic.items():
        #print '%s= %d, ' % (k, v)
        if v > statistics_max:
            statistics_max = v
        if v < statistics_min or statistics_min == 0:
            statistics_min = v
    return statistics_min, statistics_max

def calculate(key_statistics_dic, statistics_min, statistics_max):
    _range = statistics_max -  statistics_min
    #print 'max= %d, min = %d' % (_statistics_max, _statistics_min)
    feature_rate = {}
    for (k, v) in key_statistics_dic.items():
        rate = (v - statistics_min) / float (_range)
        feature_rate[k] = rate
        #print '%s= %f, ' % (k, _feature_rate[k])
    return feature_rate

def training_keys(keys_list, key_rate):
    doc_num = len(keys_list)
    p0_num = zeros(doc_num)
    p1_num = zeros(doc_num)
    i = 0
    for keys in keys_list:
        for key in keys:
            _rate = key_rate[key]
            if _rate >= 0.5:
                p1_num[i] += 1
            else:
                p0_num[i] += 1
        i += 1

    #for i in range(doc_num):
    #    print '%d line: positive = %d, negative = %d' % (i, p1_num[i], p0_num[i])

    return p1_num, p0_num

def training_by_bayes(keys_list, p0_num, p1_num):
    p1_total = sum(p1_num)
    p0_total = sum(p0_num)
    total = p1_total + p0_total
    #print 'total is %d' % (_total)

    p1_rate = p1_total / float(total)
    p0_rate = p0_total / float(total)

    doc_num = len(keys_list)
    p1_bayes = []
    p0_bayes = []
    for i in range(doc_num):
        p1 = p1_num[i]
        p0 = p0_num[i]
        p1_bayes_rate = p1 / (p1 + p0) * p1_rate / ((p1 + p0) / total)
        p0_bayes_rate = p0 / (p1 + p0) * p0_rate / ((p1 + p0) / total)
        p1_bayes.append(p1_bayes_rate)
        p0_bayes.append(p0_bayes_rate)
        #print '%d line: positive rate= %f, negative rate= %f' % (i, p1_bayes_rate, p0_bayes_rate)

    return p0_bayes, p1_bayes

def write_result(path, num, p0_bayes, p1_bayes):
    result_file = open(path, 'w')
    for i in range(num):
        p1_rate = p1_bayes[i] / sum(p1_bayes)
        p0_rate = p0_bayes[i] / sum(p0_bayes)
        clazz = 'one'
        if p1_rate < p0_rate:
            clazz = 'two'
        s = '%d line: positive= %f, negative= %f, %s\n' % (i, p1_rate, p0_rate, clazz)
        print s
        result_file.write(s)




'''
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
'''
