import json
import requests, time, random, hashlib
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .format_word import format_word

url = "http://fanyi.youdao.com/translate_o"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Referer": "http://fanyi.youdao.com/",
}

s = requests.Session()


def get_encrypt_data(keyword):
    t = "5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    bv = hashlib.md5(bytes(t, encoding="utf-8")).hexdigest()
    ts = str(int(round(time.time(), 3) * 1000))
    salt = ts + str(random.randint(1, 10))
    sign = hashlib.md5(
        bytes("fanyideskweb" + keyword + salt + "Nw(nmmbP%A-r6U3EUn]Aj", encoding="utf-8")).hexdigest()
    # print(sign)
    return ts, bv, salt, sign


def param(keyword):
    dic = {}
    dic["i"] = keyword,
    dic["from"] = "AUTO",
    dic["to"] = "AUTO",
    dic["smartresult"] = "dict",
    dic["client"] = "fanyideskweb",
    dic["doctype"] = "json",
    dic["version"] = "2.1",
    dic["keyfrom"] = "fanyi.web",
    dic["action"] = "FY_BY_REALTlME",
    dic["ts"], dic["bv"], dic["salt"], dic["sign"] = get_encrypt_data(keyword)
    return dic


def get_keywords(key):
    keyword = key
    re = s.get("http://fanyi.youdao.com/", headers=headers)
    response = s.post(url=url, data=param(keyword), headers=headers)
    a = response.json()
    return format_word(a)
