#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# learn from 零基础如何学爬虫技术 https://www.zhihu.com/question/47883186

from lxml import etree
import requests
import sys

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for a in range(1,11):
        url = 'http://cd.xiaozhu.com/search-duanzufang-p{}-0/'.format(a)
        data = requests.get(url).text
        s=etree.HTML(data)

        file=s.xpath('//*[@id="page_list"]/ul/li/div[2]/div/a/span/text()')
        sale=s.xpath('//*[@id="page_list"]/ul/li/div[2]/span[1]/i/text()')
        for i in range(24):
            title=file[i]
            price=sale[i]
            print("{} {}\n".format(title, price))


if __name__ == '__main__':
    main()