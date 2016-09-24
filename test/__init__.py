#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
import os
import unittest

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src"
sys.path.insert(0, src_dir)
sys.setdefaultencoding('utf-8')

