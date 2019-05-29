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
        self.app_pay_biz = {
            'out_trade_no': '123456789',
            'total_fee': '201',
            'body': '支付测试',
            'spbill_create_ip': '8.8.8.8',
            'notify_url': 'http://baidu.com',
        }

        self.wechat = Pay.wechat(self.config, 'app')

    def test_get_sign_key(self):
        self.assertEqual(self.wechat.config.mode, self.config.mode)

    def test_to_xml(self):
        data = {
            'a': 1,
            'b': 2,
        }
        ret = self.wechat.to_xml(data)
        self.assertEqual(ret, '<xml><a>1</a><b>2</b></xml>')

    def test_from_xml(self):
        xml_data = '<xml><a>1</a><b>2</b></xml>'
        ret = self.wechat.from_xml(xml_data)
        self.assertEqual(ret.get('a'), '1')
        self.assertEqual(ret.get('b'), '2')

    @unittest.skip
    def test_app_pay(self):
        app_biz = self.wechat.pay(self.app_pay_biz)
        print(app_biz)

    @unittest.skip
    def test_find_order(self):
        order = self.wechat.find('123456789')
        print(order)


if __name__ == '__main__':
    unittest.main()
