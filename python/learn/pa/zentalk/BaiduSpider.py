# coding=utf-8
# !/usr/bin/python

# pa zentalk cn store data from baidu, with requests + bs4
# it occurs unicode issue when use requests lib, so we use urllib2 instead

import sys
from bs4 import BeautifulSoup  # 从bs4这个库中导入BeautifulSoup
import tool
import time
import re
import urllib2


class BaiduSpider:
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

    # 请求数据
    def requestData(self, url, headers):
        req_timeout = 5
        req = urllib2.Request(url, None, headers)
        resp = urllib2.urlopen(req, None, req_timeout)
        html = resp.read()
        return html

    # analysis data
    def analysisData(self, html):
        pass
        # 使用BeautifulSoup解析这段代码
        soup = BeautifulSoup(html, "lxml")

        # analysis data
        title = soup.find("h1", class_="app-name").span.get_text()
        install_text = soup.find("span", class_="download-num").get_text()
        install = self.tool.getCount(str(install_text), "下载次数: ")

        good_eval = "NA"
        infos = soup.find("div", class_="detail").find_all("span")
        size = self.tool.replace(re.sub("大小: ", "", infos[0].get_text()))
        update = "NA"
        version = self.tool.replace(re.sub("版本:", "", infos[1].get_text()))
        upload = "NA"

        result = {}
        result["title"] = title
        result["size"] = size
        result["update"] = update
        result["version"] = version
        result["upload"] = upload
        result["install"] = install
        result["good_eval"] = good_eval

        # get comments
        commentlist = soup.find("div", class_="main").ol
        if commentlist:
            comments = commentlist.find_all("li")
            if (len(comments) > 0):
                result["comment_count"] = len(comments)
                cinfos = []
                for item in comments:
                    cinfo = {}
                    pitem_time = item.find("div", class_="comment-time")
                    cinfo["comment_time"] = pitem_time.get_text()
                    pitems_info = item.find("div", class_="comment-info").find_all("div")
                    cinfo["user"] = pitems_info[0].em.get_text()
                    cinfo["comment_des"] = pitems_info[1].p.get_text()
                    cinfos.append(cinfo)
                result["comments"] = cinfos

        return result

    def start(self, url=None, headers=None):
        if not url:
            url = "http://shouji.baidu.com/software/11306355.html"
            # 用requests的headers可以伪装成浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'close',
                'Referer': None
            }

        html = self.requestData(url, headers)
        data_dist = self.analysisData(html)
        return data_dist
