#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
from lxml import etree
import pandas
from bs4 import BeautifulSoup  # 从bs4这个库中导入BeautifulSoup
import csv
import time

zentalk_summary_url = 'http://mobile.umeng.com/apps/bff0008e977e7eacb617c785/reports/realtime_summary'
zentalk_trend = 'http://mobile.umeng.com/apps/bff0008e977e7eacb617c785/reports/trend_summary'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Host": "passport.umeng.com",
    "Refer": "http://passport.umeng.com/login",
    "Connection": "keep-alive"
}

# prepare cookie
def getCookie():
    raw_cookies = 'um_lang=zh; cna=djyZElCjejMCAXygKoKHI+4E; umlid_584654c007fe6578ca0008ef=20171121; umplus_uc_token=1fiz8Bbgt6PW4_INrDUdHxg_98da682409834b298a32fc8b3bd7d3cf; umplus_uc_loginid=randy_wang%40asus.com; cn_1258498910_dplus=%7B%22distinct_id%22%3A%20%2215fd786318ab2-00161f69ad7f42-7b113d-13c680-15fd786318c4ab%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201511245838%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201511245838%7D%2C%22initial_view_time%22%3A%20%221511244331%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fpassport.umeng.com%2Flogin%22%2C%22initial_referrer_domain%22%3A%20%22passport.umeng.com%22%7D; isg=AhUVQPnH40fXa8e6SAPxiQa4JBHFUMoTohMXL5e6ewzb7jTgX2Ln9bPmzsQj; __utmt=1; CNZZDATA1259864772=930320818-1511145113-%7C1511248082; __utma=151771813.2098797787.1511150090.1511245264.1511248926.5; __utmb=151771813.2.10.1511248926; __utmc=151771813; __utmz=151771813.1511248926.5.3.utmcsr=passport.umeng.com|utmccn=(referral)|utmcmd=referral|utmcct=/user/products; ummo_ss=BAh7CUkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjoGRVRbCEkiCVVzZXIGOwBGWwZvOhNCU09OOjpPYmplY3RJZAY6CkBkYXRhWxFpXWlLaVlpAcBpDGkB%2FmlqaX1pAcppAGkNaQHvSSIZZWdITWh1RXlGT1RtdmxGQzZ3SHkGOwBUSSIUdW1wbHVzX3VjX3Rva2VuBjsARiI9MWZpejhCYmd0NlBXNF9JTnJEVWRIeGdfOThkYTY4MjQwOTgzNGIyOThhMzJmYzhiM2JkN2QzY2ZJIhBfY3NyZl90b2tlbgY7AEZJIjFOZlJQNVFORjRHVlN4SXdwSWpURWIzTzBLQmFJdG81SlBOeERzSmQ1T29BPQY7AEZJIg9zZXNzaW9uX2lkBjsAVEkiJTM5Yzk2ZTliNTExNDQ1ZWJhMGY3OGY5YjlmZjI4NjY1BjsARg%3D%3D--5277a3cb9418daa2dcb64e86435a033948c327ba; cn_1259864772_dplus=%7B%22distinct_id%22%3A%20%2215fd786318ab2-00161f69ad7f42-7b113d-13c680-15fd786318c4ab%22%2C%22sp%22%3A%20%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3A%20false%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201511248956%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201511248956%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221511166713%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fmobile.umeng.com%2Fapps%22%2C%22initial_referrer_domain%22%3A%20%22mobile.umeng.com%22%7D; UM_distinctid=15fd786318ab2-00161f69ad7f42-7b113d-13c680-15fd786318c4ab'
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
        cookies[key] = value
    print cookies
    return cookies

# request website data
def requestData(url):
    try:
        r = requests.get(url, cookies=getCookie())
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print r.text
        return r.text
    except:
        print('无法链接服务器')


# analysis data
def analysisData(ulist, data):
    soup = BeautifulSoup(data, 'lxml')
    table = soup.find("table", class_="data-load")
    _tsoup = BeautifulSoup(str(table), 'lxml');
    thead = _tsoup.find("thead")
    tbody = _tsoup.find("tbody")
    # print thead
    print tbody


def savaToExcel(ulist):
    with open("zentalk.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['zentalk数据统计'])
        for i in range(len(ulist)):
            writer.writerow([ulist[i][0], ulist[i][1], ulist[i][2]])


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    ulist = []
    data = requestData(zentalk_trend)
    # print data
    analysisData(ulist, data)
    savaToExcel(ulist)


if __name__ == '__main__':
    main()
