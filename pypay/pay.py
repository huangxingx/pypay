#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
from pypay import err

from pypay.gateways.wechat import WechatConfig, WechatPay
from pypay.gateways.wechat_impl.app_pay_impl import AppPayImpl
from pypay.gateways.wechat_impl.mp_pay_impl import MpPayImpl
from pypay.gateways.wechat_impl.web_pay_impl import WebPayImpl


class Pay:

    @classmethod
    def ali(cls, config):
        pass

    @classmethod
    def wechat(cls, config: WechatConfig, impl_type=None) -> WechatPay:
        impl = None
        # 默认返回不带pay方法的实例
        if impl_type is None:
            impl = WechatPay

        if impl_type == 'app':
            impl = AppPayImpl

        elif impl_type == 'mp':
            impl = MpPayImpl

        elif impl_type == 'web':
            impl = WebPayImpl

        if not impl:
            raise err.InvalidArgumentException(f'Pay Type Arg Error: {impl_type} not exists impl.')

        return impl(config)
