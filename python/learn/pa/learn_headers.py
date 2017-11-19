#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup     #从bs4这个库中导入BeautifulSoup
from lxml import etree
import sys

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    link = "http://www.santostang.com/"
    # 用requests的headers可以伪装成浏览器访问
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(link, headers= headers)

    soup = BeautifulSoup(r.text, "lxml")  # 使用BeautifulSoup解析这段代码
    title = soup.find("h1", class_="post-title").a.text.strip()
    print (title)

    with open('title.txt', "a+") as f:
        f.write(title)
        f.close()

    #s = etree.HTML(r.text)
    #title = s.xpath('//*[@id="main"]/div/div[1]/article[1]/header/h1/a/text()')
    #des = s.xpath('//*[@id="main"]/div/div[1]/article[1]/div/p/text()')
    #print("{} {}\n".format(title, des))

if __name__ == '__main__':
    main()