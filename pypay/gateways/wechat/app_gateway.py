#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

from .wechatbase import WechatPayBase


class AppGateway(WechatPayBase):

    def get_trade_type(self):
        return 'APP'

    def pay(self, endpoint, payload):
        pass
