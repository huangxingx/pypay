#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
from pypay import err
from pypay.gateways.wechat import WechatConfig, WechatPay
from pypay.gateways.wechat_impl.app_pay_impl import AppPayImpl

ALI = 'ali'
WECHAT = 'wechat'


class Pay:
    wechat_config = None
    ali_config = None

    def __init__(self, config):
        self._driver = ''
        self.config = config

    @classmethod
    def get_instance(cls, driver, gateway):
        pass

    @classmethod
    def ali(cls, config):
        pass

    @classmethod
    def wechat(cls, config: WechatConfig, impl_type) -> WechatPay:
        impl = None
        if impl_type == 'app':
            impl = AppPayImpl

        if not impl:
            raise err.InvalidArgumentException(f'Pay Type Arg Error: {impl_type} not exists impl.')

        return impl(config)
