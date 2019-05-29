#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19
import time

from pypay import err
from pypay.gateways.wechat import WechatPay


class PosPayImpl(WechatPay):

    @staticmethod
    def get_trade_type():
        return 'MICROPAY'

    def pay(self, config_biz: dict):
        # todo some wrong.
        if not self.config.get('app_id'):
            raise err.InvalidArgumentException('Missing Config -- [app_id]')

        self.unset_notify_url()

        return self.request_api('pay/micropay', config_biz)
