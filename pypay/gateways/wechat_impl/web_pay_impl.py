#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19
import time

from pypay import err
from pypay.gateways.wechat import WechatPay


class WebPayImpl(WechatPay):
    """ H5 支付实现 """

    @staticmethod
    def get_trade_type():
        return 'MWEB'

    def pay(self, config_biz: dict):
        config_biz['trade_type'] = self.get_trade_type()
