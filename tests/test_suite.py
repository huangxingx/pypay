#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19


import unittest

from tests import test_wechat

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_wechat.TestWechat))

    runner = unittest.TextTestRunner(verbosity=2)

    runner.run(suite)
