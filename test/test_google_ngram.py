#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from google_ngram_downloader import readline_google_store

class TestCase(unittest.TestCase):
    def test_load_google_ngram(self):
        fname, url, records = next(readline_google_store(ngram_len=5))
        _next = True
        while _next:
            record = next(records)
            if record:
                print record
                ngram = record.ngram.encode('utf-8')
                print str(ngram)
            else:
                _next = False

unittest.main()

