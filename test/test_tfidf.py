#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __init__ import *
import unittest
import tfidf

class TestCase(unittest.TestCase):
    def test_open_stopwords_not_empty(self):
        stopwords_list = tfidf.open_stopwords()
        print stopwords_list
        self.assertTrue(len(stopwords_list) > 0)

unittest.main()

