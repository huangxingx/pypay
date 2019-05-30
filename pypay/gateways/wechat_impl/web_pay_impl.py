#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19

from urllib.parse import urlencode

from pypay.gateways.wechat import WechatPay


class WebPayImpl(WechatPay):
    """ H5 支付实现 """

    @staticmethod
    def get_trade_type():
        return 'MWEB'

    def pay(self, config_biz: dict) -> str:
        self.check_config('app_id')

        mweb_url = self.pre_order(config_biz).get('mweb_url', '')

        return_url = config_biz.get('return_url') or self.payload.get('return_url')
        if not return_url:
            return mweb_url

        return f'{mweb_url}&redirect_url={urlencode(return_url)}'
