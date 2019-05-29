#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19
import time

from pypay import err
from pypay.gateways.wechat import WechatPay


class ScanPayImpl(WechatPay):
    """ 扫码支付实现 """

    @staticmethod
    def get_trade_type():
        return 'NATIVE'

    def pay(self, config_biz: dict):
        return self.pre_order(config_biz)
