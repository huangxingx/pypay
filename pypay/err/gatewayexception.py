#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19


class InvalidGatewayException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass


class GatewayException(Exception):
    pass


class BusinessException(Exception):
    pass


class InvalidSignException(Exception):
    pass
