#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

from .gateway import Gateway


class AppGateway(Gateway):

    def pay(self, endpoint, payload):
        pass

    def pre_order(self, payload):
        super().pre_order(payload)

    def get_trade_type(self):
        return 'APP'

