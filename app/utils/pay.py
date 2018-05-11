from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from base64 import decodebytes, encodebytes
import json

class Alipay(object):
    def __init__(self, appid, app_notify_url, app_private_key_path,
            alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.alipay_public_key_path) as fp:
            self.app_private_key = RSA.importkey(fp.read())
        self.alipay_public_key = None
        with open(alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importkey(fp.read())
        if debug:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kawgs):
        biz_content = {
                "subject": subject,
                "out_trade_no": out_trade_no,
                "total_amount": total_amount,
                "product_code": "FAST_INSTANT_TRADE_PAY",
                }
        biz_content.update(kawgs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
                "app_id": self.appid,
                "method": method,
                "charset": "utf-8",
                "sign_type": "RSA2",
                "timestramp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0",
                "biz_content": biz_content
                }
        if return_url:
            data['notify_url'] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for k, v in data.items():
            if isinstance(v, dict):
                complex_keys.append(k)

        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k,v) for k,v in data.items()])

    def sign(self, unsigned_string):
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = string.sign(SHA256.new(unsigned_string))
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)

