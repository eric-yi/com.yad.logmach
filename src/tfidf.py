#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from os import listdir
from os.path import isfile, join

STOPWORDS_DIR = '../conf/stopword'

def open_stopwords():
    stopwords_files = [join(STOPWORDS_DIR, f) for f in listdir(STOPWORDS_DIR) if isfile(join(STOPWORDS_DIR, f))]
    stopwords_list = [open(f, 'r').readlines() for f in stopwords_files]
    return [s.strip().lower() for stopwords in stopwords_list for s in stopwords]


def invoke_idf(base, tf):
    file_list = filter(lambda f: f.endswith('.doc'), os.listdir(base))
    path_list = map(lambda f: base+'/'+f, file_list)
    docs = []
    for path in path_list:
        rs = open(path, 'r')
        docs.append(map(lambda x: x.strip().lower(), rs.readlines()))

    _idf = {}
    for key in tf.keys():
        _idf[key] = 0
        for doc in docs:
            if key in doc[0].lower():
                _idf[key] = 1
                break

    return _idf

def invoke_wash(strs, stop_words):
    _splits = strs.split()
    debug(_splits)
    wash_list = []
    size = len(_splits)
    #delete stop word
    splits = []
    for _split in _splits:
        if _split.lower() not in stop_words:
            splits.append(_split)

    _size = len(splits)
    m = r
    while m < _size:
        _next = m + _n
        entry = splits[m : _next]
        wash_list.append(entry)
        m += 1

    return wash_list

def invoke_tf(wash_list):
    tf = {}
    for wash in wash_list:
        wash_str = wash[0]
        if not tf.has_key(wash_str):
            tf_size = len(filter(lambda w: w[0]==wash_str, wash_list))
            #debug('wash size ' + wash_str + ':' + str(tf_size))
            tf[wash_str] = tf_size

    wash_size = len(wash_list)
    for key in tf:
        tf[key] = float(tf[key]) / wash_size


    return tf

def invoke_tfidf(tf, idf):
    _tfidf = {}
    for key in tf.keys():
        _tfidf[key] = tf[key] * idf[key]

    return _tfidf


def invoke():
    stopwords_list = open_stopwords()
    wash_list = invoke_wash(_text_exmaple, stopwords_list)
    tf = invoke_tf(wash_list)
    idf = invoke_idf('resources', tf)
    tfidf = invoke_tfidf(tf, idf)
    return tfifd

