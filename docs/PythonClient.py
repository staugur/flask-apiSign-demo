# -*- coding: utf-8 -*-
#
# Python Client
#

import hashlib, datetime, time

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))

class RequestClient(object):
    """ 接口签名客户端示例 """

    def __init__(self):
        self._version = "v1"
        self._accesskey_id = "demo_id"
        self._accesskey_secret = "demo_secret"

    def _sign(self, parameters):
        """ 签名
        @param parameters dict: uri请求参数(包含除signature外的公共参数)
        """
        if "signature" in parameters:
            parameters.pop("signature")
        # NO.1 参数排序
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])
        # NO.2 排序后拼接字符串
        canonicalizedQueryString = ''
        for (k, v) in _my_sorted:
            canonicalizedQueryString += '{}={}&'.format(k,v)
        canonicalizedQueryString += self._accesskey_secret
        # NO.3 加密返回签名: signature
        return md5(canonicalizedQueryString).upper()

    def make_url(self, params={}):
        """生成请求参数
        @param params dict: uri请求参数(不包含公共参数)
        """
        if not isinstance(params, dict):
            raise TypeError("params is not a dict")
        # 获取当前时间戳
        timestamp = get_current_timestamp() - 4
        # 设置公共参数
        publicParams = dict(accesskey_id=self._accesskey_id, version=self._version, timestamp=timestamp)
        # 添加加公共参数
        for k,v in publicParams.iteritems():
            params[k] = v
        uri = ''
        for k,v in params.iteritems():
            uri += '{}={}&'.format(k,v)
        uri += 'signature=' + self._sign(params)
        return uri

    def request(self):
        """测试用例"""
        import requests
        params = dict(c=3,d=4,b=2,a=1)
        url = 'http://127.0.0.1:1798/?'+self.make_url(params)
        return requests.get(url).json()
