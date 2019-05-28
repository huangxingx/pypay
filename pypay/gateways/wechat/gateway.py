#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
import abc


class Gateway:
    """ 抽象类 """

    def pre_order(self, payload: dict):
        payload['sign'] = Support.gen_sign(payload)

    @abc.abstractmethod
    def get_trade_type(self):
        pass

    @abc.abstractmethod
    def pay(self, endpoint, payload):
        pass
