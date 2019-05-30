# pypay
[![Build Status](https://travis-ci.org/huangxingx/pypay.svg?branch=master)](https://travis-ci.org/huangxingx/pypay)
[![codecov](https://codecov.io/gh/huangxingx/pypay/branch/master/graph/badge.svg)](https://codecov.io/gh/huangxingx/pypay)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/huangxingx/pypay/blob/master/LICENSE)

 Ali Pay And Wechat Pay With Python.

 项目移植于 [yansongda/pay](https://github.com/yansongda/pay)

## 功能
### 1、支付宝
<!-- - 电脑支付  -->
<!-- - 手机网站支付 -->
<!-- - APP 支付 -->
<!-- - 刷卡支付 -->
<!-- - 扫码支付 -->
<!-- - 账户转账 -->
<!-- - 小程序支付 -->

### 2、微信
 - 公众号支付
<!-- - 小程序支付 -->
 - H5 支付
<!-- - 扫码支付 -->
<!-- - 刷卡支付 -->
- APP 支付
<!-- - 企业付款 -->
<!-- - 普通红包 -->
<!-- - 分裂红包 -->

## 开发环境配置
```shell
pip3 install pipenv
pipenv install
```

## 使用说明

### 微信
```python

config = WechatConfig(
            appid='wxfxxxxxxxxxxxxxx',
            mch_id='137xxxxxxx',
            key='q1w2xxr4xxy6uxxxxxxxxxx',
            mode='dev'
        )

app_pay_biz = {
    'out_trade_no': '123456789',
    'total_fee': '201',
    'body': '支付测试',
    'spbill_create_ip': '8.8.8.8',
    'notify_url': 'http://baidu.com',
}

app_wechat = Pay.wechat(self.config, 'app')
app_wechat.pay(app_pay_biz)

```



### 所有异常

* err\gatewayexception\InvalidGatewayException ，表示使用了除本 SDK 支持的支付网关。
* err\gatewayexception\InvalidSignException ，表示验签失败。
* err\gatewayexception\InvalidConfigException ，表示缺少配置参数，如，`ali_public_key`, `private_key` 等。
* err\gatewayexception\GatewayException ，表示支付宝/微信服务器返回的数据非正常结果，例如，参数错误，对账单不存在等。


## LICENSE
MIT
