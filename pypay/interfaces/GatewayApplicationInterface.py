#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

import abc


class GatewayApplicationInterface:

    @abc.abstractmethod
    def pay(self, gateway: str, params: dict):
        """ 支付

        :param str gateway: 支付网关
        :param dict params:  支付参数
        :return:
        """

    @abc.abstractmethod
    def find(self, order: dict, refund):
        """ 查询订单

        :param order:
        :param refund:
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
    def close(self, order: dict):
        """ 关闭订单

        :param order:
        :return:
        """

    @abc.abstractmethod
    def verify(self, content: str, refund):
        """ 验证消息内容

        :param content:
        :param refund:
        :return:
        """

    @abc.abstractmethod
    def success(self):
        """ 通知返回

        :return: str
        """
