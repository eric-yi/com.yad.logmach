#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __init__ import *
import fetcher
from re import *

class TestCase(unittest.TestCase):
    TEST_STR = '[3/16/16 9:42:46:066 CST] 000000b7 SystemOut     O 2016-03-16 09:42:46.066 INFO    c.y.i.d.s.impl.BoseraServiceImpl:277 - BoseraServiceImpl.qryAsset-请求参数明文：{"contractNo":"205ftzex20151229017581","applyId":"ftzexc199d6e5e03047fcabb2c39a132b25d0","opType":"QRY002"}'

    @unittest.skip('skip')
    def test_fetch(self):
        fetcher.fetch('../logs/00.log')
        self.assertTrue(True)

    @unittest.skip('skip')
    def test_match_date(self):
        _data = '[3/16/16 9:42:46:069 CST] 000000b7'
        pattern = compile('^\[\d{1,2}/\d{1,2}/\d{2}')
        self.assertTrue(pattern.match(_data))

    @unittest.skip('skip')
    def test_split_by_date(self):
        _date_pattern = '\[\d{1,2}/\d{1,2}/\d{2}\s\d{1,2}:\d{2}:\d{2}:\d{3}\s\S{0,}\]\s'
        _splits = split(_date_pattern, self.TEST_STR)
        self.assertEquals(len(_splits), 2)

    @unittest.skip('skip')
    def test_split_log_item(self):
        _date_pattern = '\[\d{1,2}/\d{1,2}/\d{2}\s\d{1,2}:\d{2}:\d{2}:\d{3}\s\S{0,}\]'
        _result = fetcher.split_log_item(_date_pattern, self.TEST_STR)
        print _result[0]
        print _result[1]
        self.assertEquals(len(_result), 2)

    #@unittest.skip('skip')
    def test_split_log(self):
        patterns = [
            '\[\d{1,2}/\d{1,2}/\d{2}\s\d{1,2}:\d{2}:\d{2}:\d{3}\s\S*\]\s+',
            '\w+\s+',
            '\S+\s+',
            '\S+\s+'
        ]
        _result = fetcher.split_log(patterns, self.TEST_STR)
        for item in _result:
            print item
        self.assertEquals(len(_result), len(patterns)+1)

unittest.main()
