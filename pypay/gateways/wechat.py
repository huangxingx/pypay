#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:28/05/19
import abc
import hashlib
import random
from enum import Enum

import requests

from pypay import err
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


class WechatPay(GatewayApplicationInterface):
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
            'mch_id': self.config.mch_id,
            'nonce_str': self.gen_nonce_str(),
            'sign_type': 'MD5',
            'notify_url': self.config.notify_url,
            'trade_type': self.get_trade_type(),
        }

        self.set_dev_key()

    @staticmethod
    def get_trade_type():
        return ''

    def pre_order(self, config_biz: dict):

        biz = dict(self.payload, **config_biz)

        return self.request_api('pay/unifiedorder', biz)

    @abc.abstractmethod
    def pay(self, config_biz: dict):
        pass

    def find(self, out_trade_no: str):
        self.payload['out_trade_no'] = out_trade_no
        self.unset_trade_type_and_notify_url()

        return self.request_api('pay/orderquery', self.payload)

    def refund(self, order: dict):
        new_order = dict(self.payload, **order)
        new_order['op_user_id'] = new_order.get('op_user_id') if 'op_user_id' in new_order else self.payload.get(
            'mch_id', '')

        self.unset_trade_type_and_notify_url()

        return self.request_api('secapi/pay/refund', new_order, cert=True)

    def cancel(self, order: dict):
        pass

    def close(self, out_trade_no: str):
        self.payload['out_trade_no'] = out_trade_no
        self.unset_trade_type_and_notify_url()

        return self.request_api('pay/closeorder', self.payload)

    def verify(self, content: str, sign=None, sync=False):
        data = self.from_xml(content)
        sign = data.get('sign') if sign is None else sign

        return data if self.get_sign_content(data) == sign else False

    def success(self):
        ret_dict = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
        }

        return self.to_xml(ret_dict)

    def set_dev_key(self):
        """ 设置沙箱模式的key """
        if self.config.mode == WechatModeEnum.MODE_DEV.value:
            data = {
                'mch_id': self.config.mch_id,
                'nonce_str': self.gen_nonce_str()
            }

            result = self.request_api('pay/getsignkey', data)
            self.config.key = result['sandbox_signkey']

        return self

    @staticmethod
    def gen_nonce_str(length=16):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        str_list = []
        chars_len = len(chars)
        for _ in range(length):
            str_list.append(chars[random.randint(0, chars_len - 1 - 1)])

        return ''.join(str_list)

    @staticmethod
    def from_xml(data: str):
        if not data:
            return
        xml_element = ET.fromstring(data)
        dict_data = dict()
        for element_one in xml_element.iter():
            dict_data[element_one.tag] = element_one.text
        if 'xml' in dict_data:
            del dict_data['xml']
        return dict_data

    @staticmethod
    def to_xml(data: dict) -> str:
        xml_list = ['<xml>']
        for k, v in data.items():
            if isinstance(v, (str, float, int)):
                item = f'<{k}>{v}</{k}>'
            else:
                item = f'<{k}><![CDATA[{v}]]</{k}>'
            xml_list.append(item)
        xml_list.append('</xml>')
        return ''.join(xml_list)

    def gen_sign(self, data: dict):
        key = self.config.key

        if not key:
            raise err.InvalidArgumentException('Missing Wechat Config -- [key]')

        md5_str = hashlib.md5(f'{self.get_sign_content(data)}&key={key}'.encode('utf-8'))

        return md5_str.hexdigest().upper()

    @staticmethod
    def get_sign_content(data):
        return '&'.join('%s=%s' % (key, data.get(key)) for key in sorted(data) if key != 'sign' and data.get(key))

    def request_api(self, endpoint, data, cert=False):
        url = self.gateway + endpoint

        if not data.get('sing'):
            data['sign'] = self.gen_sign(data)

        # cert 证书问题
        response = requests.post(
            url,
            data=self.to_xml(data).encode(),
        )
        result = response.text if response.ok else ''
        result = self.from_xml(result)

        return self.processing_api_result(endpoint, result)

    def processing_api_result(self, endpoint, result):

        if result.get('return_code', '') != 'SUCCESS':
            raise err.GatewayException(f'Get API Error: {result.get("return_msg", "")} {result}')

        if result.get('result_code') and result.get('result_code') != 'SUCCESS':
            raise err.BusinessException(f'Wechat Business Error: {result.get("err_code", "")}')

        if endpoint == 'pay/getsignkey' or self.gen_sign(result) == result.get('sign', ''):
            return result

        raise err.InvalidSignException('Wechat Sign Verify FAILED', result)

    def unset_trade_type_and_notify_url(self):
        if 'notify_url' in self.payload:
            del self.payload['notify_url']

        if 'trade_type' in self.payload:
            del self.payload['trade_type']

        return True
