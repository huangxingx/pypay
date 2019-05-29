#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19
import time

from pypay import err
from pypay.gateways.wechat import WechatPay


class MpPayImpl(WechatPay):

    @staticmethod
    def get_trade_type():
        return 'JSAPI'

    def pay(self, config_biz: dict):
        if not self.config.get('app_id'):
            raise err.InvalidArgumentException('Missing Config -- [app_id]')

        _now = time.time()
        prepay_id = self.pre_order(config_biz).get('prepay_id')

        pay_dict = {
            'appid': self.config.appid,
            'partnerid': self.config.mch_id,
            'prepayid': prepay_id,
            'timestamp': _now,
            'noncestr': self.gen_nonce_str(),
            'package': f'prepay_id={prepay_id}'
        }
        pay_dict['paySign'] = self.gen_sign(pay_dict)

        return pay_dict
