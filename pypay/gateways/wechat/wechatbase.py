#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
import hashlib
import random
from enum import Enum

import collections
import requests

from pypay.interfaces.GatewayApplicationInterface import GatewayApplicationInterface
from pypay.util import xml_et_cdatasection as ET


class WechatModeEnum(Enum):
    """ 微信运行模式  """
    MODE_NORMAL = 'normal'  # 正常模式
    MODE_DEV = 'dev'  # 沙箱模式
    MODE_HK = 'hk'  # 香港钱包
    MODE_US = 'us'  # 境外模式
    MODE_SERVICE = 'service'  # 服务商模式


class WechatConfig:
    def __init__(self,
                 appid='',
                 app_id='',
                 miniapp_id='',
                 mch_id='',
                 key='',
                 notify_url='',
                 cert_client='',
                 cert_key='',
                 mode=WechatModeEnum.MODE_NORMAL.value,
                 ):
        self.appid = appid  # 商户绑定的appid
        self.app_id = app_id  # 公众号 app_id
        self.miniapp_id = miniapp_id  # 小程序 app_id
        self.mch_id = mch_id  # 商户号id
        self.key = key  # 商户支付秘钥
        self.notify_url = notify_url  # 通知回调 url
        self.cert_client = cert_client
        self.cert_key = cert_key
        self.mode = mode  # 运行模式


class WechatPayBase(GatewayApplicationInterface):
    URL = {
        WechatModeEnum.MODE_NORMAL.value: 'https://api.mch.weixin.qq.com/',
        WechatModeEnum.MODE_DEV.value: 'https://api.mch.weixin.qq.com/sandboxnew/',
        WechatModeEnum.MODE_HK.value: 'https://apihk.mch.weixin.qq.com/',
        WechatModeEnum.MODE_US.value: 'https://apius.mch.weixin.qq.com/',
        WechatModeEnum.MODE_SERVICE.value: 'https://api.mch.weixin.qq.com/',
    }

    def __init__(self, config: WechatConfig):
        self.config = config
        self.gateway = self.URL.get(self.config.mode)

        self.payload = {
            'appid': self.config.appid,
            'app_id': self.config.app_id,
            'mch_id': self.config.mch_id,
            'nonce_str': self.config.notify_url,
            'sign': '',
            'spbill_create_ip': '',
        }

    def get_trade_type(self):
        return ''

    def pay(self, gateway: str, params: dict):
        # self.payload.update(params)
        # gateway = f'{gateway}.Gateway'
        # try:
        #     __import__(gateway, fromlist=['gateways', 'wechat'])
        #
        # except ImportError:
        #     raise err.InvalidGatewayException(f"Pay Gateway [{gateway}] Not Exists")
        #
        # return self._make_pay(gateway)
        pass

    def find(self, order: dict, refund):
        super().find(order, refund)

    def refund(self, order: dict):
        super().refund(order)

    def cancel(self, order: dict):
        super().cancel(order)

    def close(self, order: dict):
        super().close(order)

    def verify(self, content: str, refund):
        super().verify(content, refund)

    def success(self):
        ret_dict = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
        }

        return self.to_xml(ret_dict)

    def _make_pay(self, gateway):
        app = gateway()
        if isinstance(app, GatewayInterface):
            return app.pay(self.gateway, filter(lambda k: True if self.payload[k] else False, self.payload))

        raise err.InvalidGatewayException("Pay Gateway [{$gateway}] Must Be An Instance Of GatewayInterface")

    def set_dev_key(self):
        """ 设置沙箱模式的key """
        if self.config.mode == WechatModeEnum.MODE_DEV.value:
            data = {
                'mch_id': self.config.mch_id,
                'nonce_str': self.gen_nonce_str()
            }
            data['sign'] = self.gen_sign(data)

            result = self.request_api('pay/getsignkey', data)
            self.config.key = result['sandbox_signkey']

        return self

    @staticmethod
    def gen_nonce_str(length=16):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        str_list = []
        for _ in range(length):
            str_list.append(random.choices(chars))

        return ''.join(str_list)

    @staticmethod
    def from_xml(data: str):
        if not data:
            return
        xml_element = ET.fromstring(data)
        dict_data = dict()
        for element_one in xml_element.iter():
            dict_data[element_one.tag] = element_one.text

        return dict_data

    @staticmethod
    def to_xml(data: dict) -> str:
        xml_list = ['<xml>']
        for k, v in data.items():
            if isinstance(v, str):
                item = f'<{k}>{v}<{k}>'
            else:
                item = f'<{k}><![CDATA[{v}]]<{k}>'
            xml_list.append(item)

        return ''.join(xml_list)

    def gen_sign(self, data: dict):
        key = self.config.key

        if not key:
            raise err.InvalidArgumentException('Missing Wechat Config -- [key]')

        order_data = list(collections.OrderedDict(data))
        ordered_data = sorted(order_data, key=lambda k: k[0])
        md5_str = hashlib.md5(f'{self.get_sign_content(ordered_data)}&key={key}')

        return md5_str.hexdigest().upper()

    @staticmethod
    def get_sign_content(data_dict: dict):
        str_list = []

        for k, v in data_dict.items():
            if k != 'sign' and v:
                str_list.append(f'{k}={v}')

        return ''.join(str_list)

    def request_api(self, endpoint, data, cert=False):
        url = self.gateway + endpoint
        # cert 证书问题
        response = requests.post(
            url,
            self.to_xml(data),

        )
        result = response.text if response.ok else ''
        result = self.from_xml(result)

        return self.processing_api_result(endpoint, result)

    def processing_api_result(self, endpoint, result):

        if result.get('return_code', '') != 'SUCCESS':
            raise err.GatewayException(f'Get API Error: {result.get("return_msg", "")}')

        if result.get('result_code') != 'SUCCESS':
            raise err.BusinessException(f'Wechat Business Error: {result.get("err_code", "")}')

        if endpoint == 'pay/getsignkey' or self.gen_sign(result) == result.get('sign', ''):
            return result

        raise err.InvalidSignException('Wechat Sign Verify FAILED', result)
