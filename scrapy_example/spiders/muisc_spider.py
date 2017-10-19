# -*- coding: utf-8 -*-
# code by 曳光剂

import scrapy
import json
import base64

import time
from Crypto.Cipher import AES


class BooksSpider(scrapy.Spider):
    name = "muisc"
    page = 0

    def start_requests(self):
        yield self.to_request()

    def parse(self, response):
        json_dict = json.loads(response.body_as_unicode())
        print("第" + str(self.page / 20))
        try:
            for item in json_dict['comments']:
                time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['time'] / 1000))
                if item['user']['nickname'] == "曳光剂":
                    print("%s 说：%s ,时间：%s" % (item['user']['nickname'], item['content'], time1))
                    return
            self.page = self.page + 20
            yield self.to_request()
        except KeyError:
            print(json_dict)

    def to_request(self):
        first_param = '{rid:\"\", offset: \"%s\", total:\"true\", limit:\"20\", csrf_token:\"\"} ' % self.page
        return scrapy.FormRequest(
            url="http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016?csrf_token=9db84dfc080a17b3078c5bd4a76d4cc4",
            headers=headers
            , formdata={
                "params": get_params(first_param),
                "encSecKey": get_encSecKey()
            }, callback=self.parse)


headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"


def get_params(first_param):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8")
    return encrypt_text
