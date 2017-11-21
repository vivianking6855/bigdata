#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-21 09:33:22
# Project: DouBanSpider
# learn from pyspider 爬虫教程（一）：HTML 和 CSS 选择器 https://segmentfault.com/a/1190000002477863

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url = 'http://movie.douban.com/tag/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.base_url, callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": [x.text() for x in response.doc('h3').items()],
            "des": response.doc('.article > div').text(),
        }
