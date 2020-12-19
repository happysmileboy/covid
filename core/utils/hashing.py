# -*- coding:utf-8 -*-

import hmac
import hashlib
import base64


def get_signature(http_method, api_path, nonce, timestamp, api_secret_key, body: object=None):
    '''
    :param api_secret_key:
    '''
    req_body = ''
    if body is not None:
        ls = []
        for key, value in body.items():
            ls.append(f'{key}={value}')
        sorted_ls = sorted(ls)
        i = 0
        for item in sorted_ls:
            if i == 0:
                req_body += '?' + item
            else:
                req_body += '&' + item
            i+=1


    value = f'{nonce}{timestamp}{http_method}{api_path}{req_body}'.encode()
    key = api_secret_key.encode()
    h = hmac.new(key, value, hashlib.sha512)
    return base64.b64encode(h.digest()).decode()
