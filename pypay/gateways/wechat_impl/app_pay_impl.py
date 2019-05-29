#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
import time

from pypay.gateways.wechat import WechatPay


class AppPayImpl(WechatPay):

    def get_trade_type(self):
        return 'APP'

    def pay(self, config_biz) -> dict:
        """

        :param pay_type:
        :param config_biz:
                - 商品描述	body
                - 商户订单号	out_trade_no
                - 总金额	total_fee
                - 终端IP	spbill_create_ip
                - 通知地址	notify_url
        :return:
        """

        _now = time.time()
        prepay_id = self.pre_order(config_biz).get('prepay_id')

        pay_dict = {
            'appid': self.config.appid,
            'partnerid': self.config.mch_id,
            'prepayid': prepay_id,
            'timestamp': _now,
            'noncestr': self.gen_nonce_str(),
            'package': 'Sign=WXPay'
        }

        pay_dict['sign'] = self.gen_sign(pay_dict)

        return pay_dict
