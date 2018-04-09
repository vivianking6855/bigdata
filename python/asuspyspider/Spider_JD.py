#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-28 10:48:50
# Project: JD Spider template

import sys

# system print config for chinese
reload(sys)
sys.setdefaultencoding('utf-8')
import uniout

# specify project path
project_paths = [unicode("D:\\android_developer\\BigData\\python", "utf-8"),
                 unicode("F:\\Manager\\大数据\\Code\\localgit\\python", "utf-8"),
                 unicode("D:\\Project\\大数据\\BigData\\python", "utf-8")]
for p in project_paths:
    sys.path.append(p)

from asuspyspider.BaseJD import *

# debug, True:save local db; otherwise save to remote db
DEBUG = True
# config file path
CONFIG_FILE = "zenbo_config.json"
CONFIG_PATH = tool.resolveProjectPath(project_paths) + os.sep + cm.CONFIGS_PATH + os.sep + CONFIG_FILE
POS = 0
# spider time, default set to 12 * 60, 24小时抓取一次
TIME = 12 * 60  # 抓取频率, 有效期 (/分)


class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }
    }

    def __init__(self):
        # init BaseOperation
        configJson = tool.readConfigFromFile(CONFIG_PATH)
        cfg = configJson[cm.CONFIGS][POS]
        self.baseOperation = BaseOperation()
        self.baseOperation.init_config(cfg, DEBUG)

    @every(minutes=TIME)  # 每小时
    def on_start(self):
        self.crawl(self.baseOperation.url, callback=self.index_page, validate_cert=False, fetch_type='js')

    # 搜索出的列表页面
    @config(age=TIME * 60)
    @config(priority=4)
    def index_page(self, response):
        self.baseOperation.index_page(self, response)

    # 搜索翻页页面
    @config(age=TIME * 60)
    @config(priority=3)
    def turn_page(self, response):
        self.baseOperation.turn_page(self, response)

    @config(age=TIME * 60)
    @config(priority=2)
    def detail_page(self, response):
        self.baseOperation.detail_page(self, response)
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    # we get comments through json api
    @config(age=TIME * 60)
    @config(priority=1)
    def comment_page(self, response):
        self.baseOperation.comment_page(self, response)
