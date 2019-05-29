#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
from pypay.gateways.wechat.wechatbase import WechatConfig
from pypay.gateways.wechat.wechatbase import WechatPayBase


class Pay:

    @staticmethod
    def alipay(config):
        pass

    @staticmethod
    def wechat(config: WechatConfig) -> WechatPayBase:
        return WechatPayBase(config)

    def gateway(self, gateway_type):

        if gateway_type == 'app':
            return