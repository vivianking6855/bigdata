#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("http://httpbin.org/post", data=payload)
print r.text

url = 'http://www.baidu.com'
r = requests.get(url)
print r.cookies

url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print r.text

r = requests.get('https://github.com', verify=True)
print r.text