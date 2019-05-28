#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

import unittest
from pypay.pay import Pay, WechatConfig


class TestWechat(unittest.TestCase):

    def setUp(self):
        self.config = WechatConfig(

        )
        self.wechat = Pay.wechat(self.config)

    def test_get_sign_key(self):
        self.assertEqual(self.wechat.config.mode, 'normal')
