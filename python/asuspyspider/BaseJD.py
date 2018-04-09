# -*- encoding: utf-8 -*-
"""
JD opration base class, parse and save product and comments data
"""

from pyspider.libs.base_handler import *
import json
import os
import re

import utils.common as cm
import utils.dbhelper as dbhelper
import utils.tool as tool


class BaseOperation:
    spider_time = tool.getCurrentIntTime()
    spider_timestr = tool.getCurrentTime()

    # config include product's information
    def init_config(self, config, debug):
        search_word = config[cm.SEARCH_WORD]
        # product name, will show on result website
        self.productName = config[cm.PRODUCT_NAME]
        # key word, to filter product again
        self.keyword = config[cm.KEY_WORD]
        # whether only care 自营 product
        self.jdown = config[cm.JDOWN]
        price = config[cm.PRICE]
        # psort=4 按照评论数排序;psort=1 按照价格排序;
        self.url = 'https://search.jd.com/Search?keyword=' + search_word + '&enc=utf-8&wq=' + search_word + '&ev=exprice_' + price + 'gt%5E&psort=4&click=0'
        # comment json api url
        self.comment_url = "https://club.jd.com/comment/skuProductPageComments.action?productId="
        # 翻页 url
        self.turnpage_url = self.url + '&page='
        self.tool = tool.Tool()
        self.mysql = dbhelper.MySQLDBHelp(debug, config[cm.TABLES])
        print "BaseOperation init_config"

    # get visiable number in detail page
    def getVisiableNumber(self, pages):
        list = []
        list.append(0)
        for each in pages:
            numstr = each.text()
            if numstr.isdigit():
                num = int(numstr)
                list.append(num)
        return max(list)

    def index_page(self, client, response):
        try:
            page = response.doc('.fp-text > i').text()
            print "search total page:", page
            for i in range(1, int(page) + 1):
                num = i * 2 - 1
                turn_page = self.turnpage_url + str(num)
                print "search page :", i, ",", turn_page
                client.crawl(turn_page, callback=client.turn_page, validate_cert=False, fetch_type='js',
                             save={'page': i})
        except Exception, e:
            print "index_page fail:", e

    def turn_page(self, client, response):
        try:
            page = response.save.get('page')
            plist = response.doc('.J-goods-list > .clearfix >li')
            index = 1
            for each in plist.items():
                # 仅抓取JD自营商品
                jd_own = each.find('.p-icons>i.goods-icons.J-picon-tips.J-picon-fix')
                if not self.jdown or (jd_own and jd_own.text() == unicode("自营","utf-8")):
                    name = each.find('.p-name-type-2 em').text()
                    if self.keyword in name:
                        detail_url = each.find('.p-commit > strong > a').attr("href")
                        print "search page :", page, ",product index:", index, ",url", detail_url
                        index = index + 1
                        client.crawl(detail_url, callback=client.detail_page, validate_cert=False, fetch_type='js')
        except Exception, e:
            print "turn_page fail:", e

    def detail_page(self, client, response):
        productId = re.findall("/\d+.html", response.url)[0]
        productId = re.findall("\d+", productId)[0]
        print "product:", productId, ",", response.url

        # write part product info to db
        dict = {}
        dict['productName'] = self.productName
        dict['productId'] = productId
        dict['displayName'] = response.doc('.sku-name').text()
        dict['detailUrl'] = response.url
        dict['price'] = response.doc('.p-price > span').eq(1).text()
        self.add_product(dict)

        # 采用递归方式,直到返回空的comments或者到达100页;JD 最多返回100页数据,超过返回空
        multi_url = self.comment_url + productId + "&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1"
        client.crawl(multi_url, callback=client.comment_page, validate_cert=False, fetch_type='js',
                     save={'page': 0, 'productId': productId})

    def comment_page(self, client, response):
        try:
            # get page position information
            page = response.save.get('page')
            productId = response.save.get('productId')
            print "comment page:", page, ",product", productId, ",", response.url

            # json parse
            jsonstr = response.doc("body").text()
            hjson = json.loads(jsonstr)
            comments = hjson["comments"]
            summary = hjson["productCommentSummary"]
            # comments list infomation
            commentslist = []
            commentsIds = []
            for each in comments:
                time_int = tool.dateTimeToInt(each["creationTime"])  # convert comment time to timestamp
                data = (productId, each["id"], each["nickname"], time_int, each["creationTime"], each["score"],
                        each["userLevelName"], each['userImgFlag'], each["content"])
                commentslist.append(data)
                commentsIds.append(each["id"])

            # if last page, write product in db. JD max page is 100, it will return empty comments if page > 100
            if len(commentsIds) == 0 or page >= 100:
                print "it's the last page, write product in db"
                dict_sum = {}
                dict_sum['productId'] = productId
                dict_sum['goodCount'] = summary['goodCount']
                dict_sum['generalCount'] = summary['generalCount']
                dict_sum['poorCount'] = summary['poorCount']
                self.supplement_product(dict_sum)
            else:
                # write comments to db
                self.add_comments(commentslist, productId)
                # goto next page
                page = page + 1
                multi_url = self.comment_url + str(productId) + "&score=0&sortType=5&page=" + str(
                    page) + "&pageSize=10&isShadowSku=0&rid=0&fold=1"
                client.crawl(multi_url, callback=client.comment_page, validate_cert=False, fetch_type='js',
                             save={'page': page, 'productId': productId})
        except Exception, e:
            print "comment_page ex ", e
            # goto next page
            page = page + 1
            multi_url = self.comment_url + str(productId) + "&score=0&sortType=5&page=" + str(
                page) + "&pageSize=10&isShadowSku=0&rid=0&fold=1"
            client.crawl(multi_url, callback=client.comment_page, validate_cert=False, fetch_type='js',
                         save={'page': page, 'productId': productId})

    # write product info to db: price,url,displayname
    def add_product(self, dict):
        dict['updateTime'] = BaseOperation.spider_time
        dict['updateTimeStr'] = BaseOperation.spider_timestr
        self.mysql.add_product(dict)

    # supplement product info : updateTime,goodCount, etc.
    def supplement_product(self, dict):
        dict['updateTime'] = BaseOperation.spider_time
        dict['updateTimeStr'] = BaseOperation.spider_timestr
        self.mysql.supplement_product(dict)

    # add comments
    def add_comments(self, commentslist, productId):
        self.mysql.add_comments(commentslist, productId)
