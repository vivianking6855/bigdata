# coding=utf-8
# !/usr/bin/python

# pa zentalk cn store data from wandoujia, with requests + bs4

import sys
import requests
from bs4 import BeautifulSoup  # 从bs4这个库中导入BeautifulSoup
import tool
import time


class WandoujiaSpider:
    def __init__(self):
        self.tool = tool.Tool()
        reload(sys)
        sys.setdefaultencoding('utf-8')

    # 获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def requestData(self, url, headers):
        r = requests.get(url, headers=headers)
        return r

    def analysisData(self, html):
        # analysis data
        soup = BeautifulSoup(html.text, "lxml")  # 使用BeautifulSoup解析这段代码

        # analysis data
        title = soup.find("p", class_="app-name").span.get_text()
        installtext = soup.find("span", class_="item install").i.get_text()
        install = self.tool.getCount(installtext)
        good_eval = soup.find("span", class_="item love").i.get_text()
        infos = soup.find("dl", class_="infos-list").find_all("dd")
        size = self.tool.replace(infos[0].get_text())
        update = self.tool.replace(infos[3].get_text())
        version = self.tool.replace(infos[4].get_text())
        upload = self.tool.replace(infos[6].get_text())

        result = {}
        result["title"] = title
        result["size"] = size
        result["update"] = update
        result["version"] = version
        result["upload"] = upload
        result["install"] = install
        result["good_eval"] = good_eval

        # get comments
        comments = soup.find("ul", class_="comments-list").find_all("li")
        if (len(comments) - 1 > 0):
            result["comment_count"] = len(comments) - 1
            cinfos = []
            for item in comments:
                pitems = item.find_all("p")
                if (len(pitems) > 0):
                    cinfo = {}
                    nitems = pitems[0].find_all("span")
                    cinfo["user"] = nitems[0].get_text()
                    cinfo["comment_time"] = nitems[1].get_text()
                    cinfo["comment_des"] = pitems[1].span.get_text()
                    cinfos.append(cinfo)
            result["comments"] = cinfos

        return result

    def start(self, url=None, headers=None):
        if not url:
            url = "http://www.wandoujia.com/apps/com.asus.cnzentalk"
            # 用requests的headers可以伪装成浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

        html = self.requestData(url, headers)
        data_dist = self.analysisData(html)
        return data_dist
