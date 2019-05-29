#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

import abc


class GatewayApplicationInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pay(self, params: dict):
        """ 支付

        :param dict params:  支付参数
        :return:
        """

    @abc.abstractmethod
    def find(self, out_trade_no: str):
        """ 查询订单

        :param out_trade_no:
        :return:
        """
        pass

    @abc.abstractmethod
    def refund(self, order: dict):
        """ 退款

        :param order:
        :return:
        """
        pass

    @abc.abstractmethod
    def cancel(self, order: dict):
        """ 取消订单

        :param order:
        :return:
        """
        pass

    @abc.abstractmethod
    def close(self, out_trade_no: str):
        """ 关闭订单

        :param out_trade_no:
        :return:
        """

    @abc.abstractmethod
    def verify(self, content: str, sign=None, sync=False):
        """ 验证消息内容

        :param content:
        :param sync:
        :param sign:
        :return:
        """

    @abc.abstractmethod
    def success(self):
        """ 通知返回

        :return: str
        """
