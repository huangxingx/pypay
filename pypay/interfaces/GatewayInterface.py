#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19

import abc


class GatewayInterface:

    @abc.abstractmethod
    def pay(self, endpoint, payload):
        pass
