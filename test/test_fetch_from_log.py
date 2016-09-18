#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __init__ import *
import operator
import unittest

class TestCase(unittest.TestCase):
    def test_fetch_from_log(self):
        _file = open('../logs/0.log', 'r')
        content = []
        _total_size = 0
        for _line in _file:
            _row = _line.split(' ')
            _total_size += len(_row)
            content.append(_row)
        _file.close()

        print 'total size: %d' % (_total_size)

        _word_values = {}
        l = 0
        for _row in content:
            c = 0
            _last = ''
            _next = ''
            for _word in _row:
                _word_value = WordValue()
                _word_value._last = _last
                _word_value._line = l
                _word_value._column = c
                if c < len(_row) - 1:
                    _next = _row[c+1]
                _word_value._next = _next
                if _word not in _word_values.keys():
                    _word_values[_word] = []
                _word_values[_word].append(_word_value)
                _last = _word

        print 'word value have %d items' % (len(_word_values))
        _sorted_word_values = sorted(_word_values, key=lambda v: len(_word_values[v]), reverse=True)
        #_first_key = _sorted__word_values.keys()[0]
        #print 'first value:%s, found it in %d items' % (_first_key, len(_sorted_word_values[_first_key]))
        #print '%s: %d'% ('SystemOut', len(_word_values['SystemOut']))

        limit = 0
        for _word_key in _sorted_word_values:
            print '%s: %d'% (_word_key, len(_word_values[_word_key]))
            while limit >= 10:
                break
            limit += 1


class WordValue:
    _last = ''
    _next = ''
    _line = -1
    _column = -1

    def __str__(self):
        return '_last:%s, _next:%s, _line:%d, _column:%d' % (self._last, self._next, self._line, self._column)

unittest.main()
