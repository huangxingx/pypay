#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:29/05/19


import abc


class PayInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pay(self, endpoint, payload):
        pass
