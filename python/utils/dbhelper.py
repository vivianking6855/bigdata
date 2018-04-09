# -*- coding: utf-8 -*-

"""
mysql db 处理类
"""

import MySQLdb
from snownlp import SnowNLP

import common

import datetime


class MySQLDBHelp:
    KEY_HOST = 'hosts'
    KEY_USERNAME = 'username'
    KEY_PASSWORD = 'password'
    KEY_DATABASE = 'database'
    KEY_CHARSETS = 'charsets'
    # 新增comment每次仅比较最多一个月前的comment，更早之前忽略
    COMMENT_TIME_THRESHOLD = datetime.timedelta(days=30)

    def __init__(self, debug, tables):
        self.table_info = tables[common.TABLE_INFO_INDEX]
        self.table_info_sub = tables[common.TABLE_SUB_INFO_INDEX]
        self.table_comments = tables[common.TABLE_COMMENTS_INDEX]
        self.table_comments_sub = tables[common.TABLE_COMMENTS_SUB_INDEX]
        # print "tables:",tables
        self.LocalTestConfig = {
            MySQLDBHelp.KEY_HOST: 'localhost',  # 数据库主机地址
            MySQLDBHelp.KEY_USERNAME: 'root',  # 数据库用户名
            MySQLDBHelp.KEY_PASSWORD: '123456',  # 数据库密码
            MySQLDBHelp.KEY_DATABASE: 'nms',  # 数据库db名字
            MySQLDBHelp.KEY_CHARSETS: 'utf8'
        }

        self.ServerConfig = {
            MySQLDBHelp.KEY_HOST: '填入自己的Host',
            MySQLDBHelp.KEY_USERNAME: '填入自己的用户名',
            MySQLDBHelp.KEY_PASSWORD: '填入自己的密码',
            MySQLDBHelp.KEY_DATABASE: '填入自己的DB',
            MySQLDBHelp.KEY_CHARSETS: 'utf8'
        }
        if debug:
            self.dbConnectConfig = self.LocalTestConfig
        else:
            self.dbConnectConfig = self.ServerConfig
        # connect
        # print self.dbConnectConfig
        self.connect()

    # connect to mysql db
    def connect(self):
        try:
            self.conn = MySQLdb.connect(host=self.dbConnectConfig[MySQLDBHelp.KEY_HOST],
                                        user=self.dbConnectConfig[MySQLDBHelp.KEY_USERNAME],
                                        passwd=self.dbConnectConfig[MySQLDBHelp.KEY_PASSWORD],
                                        db=self.dbConnectConfig[MySQLDBHelp.KEY_DATABASE],
                                        charset=self.dbConnectConfig[MySQLDBHelp.KEY_CHARSETS])
            self.cursor = self.conn.cursor()
        except Exception, e:
            print "connect fail! ", e

    # add product info: price, display name, detail url. because these information can't be found in comment json api
    def add_product(self, dict):
        try:
            # check if product exist
            sql_query = "select productId from " + self.table_info + " where productId=" + str(dict['productId'])
            self.cursor.execute(sql_query)
            # if exist, do nothing
            if self.cursor.fetchone():
                print "product exists, update info."
                # update info table
                data = (dict['displayName'], dict['detailUrl'], dict['price'], dict['productId'])
                sql_update = "update " + self.table_info + " set displayName=%s,detailUrl=%s,price=%s where productId=%s"
                self.cursor.execute(sql_update, data)
                self.conn.commit()
            # if no product, add it
            else:
                print "no product, add it"
                data = (dict['productId'], dict['productName'], dict['displayName'], dict['detailUrl'], dict['price'])
                sql_insert = "insert into " + self.table_info + "(productId,productName,displayName,detailUrl,price) values(%s,%s,%s,%s,%s);"
                self.cursor.execute(sql_insert, data)
                self.conn.commit()

            # insert to update info sub
            print "add product info to sub table"
            data = (dict['productId'], dict['productName'], dict['price'], dict['updateTime'], dict['updateTimeStr'])
            sql_sub_insert = "insert into " + self.table_info_sub + "(productId,productName,price,updateTime,updateTimeStr) values(%s,%s,%s,%s,%s);"
            self.cursor.execute(sql_sub_insert, data)
            self.conn.commit()

        except Exception, e:
            print "add_product fail! ", e

    # insert into db
    def supplement_product(self, dict):
        try:
            # update time and goodCount, etc. product info table
            data_update = (
                dict['updateTime'], dict['updateTimeStr'], dict['goodCount'], dict['generalCount'], dict['poorCount'],
                dict['productId'])
            sql_update = "update " + self.table_info + " set updateTime=%s,updateTimeStr=%s,goodCount=%s,generalCount=%s," \
                                                       "poorCount=%s where productId=%s"
            self.cursor.execute(sql_update, data_update)
            self.conn.commit()
            # update time and goodCount, etc. product sub info table
            data_update = (
                dict['goodCount'], dict['generalCount'], dict['poorCount'], dict['productId'], dict['updateTime'])
            sql_update = "update " + self.table_info_sub + " set goodCount=%s,generalCount=%s,poorCount=%s where productId=%s and updateTime=%s"
            self.cursor.execute(sql_update, data_update)
            self.conn.commit()
        except Exception, e:
            print "supplement_product fail! ", e

    # add comments to db and analysis them when save
    def add_comments(self, commentslist, productId):
        try:
            # check if time > last spider time
            sql_query = "select updateTime from " + self.table_info + " where productId=" + str(productId)
            self.cursor.execute(sql_query)
            row = self.cursor.fetchone()
            print "productId:", productId, ",updateTime:", row
            if row:
                # product update time exist
                last_spider_time = datetime.datetime.fromtimestamp(row[0])
                comments = []
                for each in commentslist:
                    comment_time = datetime.datetime.fromtimestamp(each[3])
                    # 新增comment每次仅比较最多一个月前的comment，更早之前忽略
                    if last_spider_time - comment_time <= MySQLDBHelp.COMMENT_TIME_THRESHOLD:
                        if self.queryComment(each[1], productId) == 0:  # comment not in db
                            comments.append(each)
                self.addNewComments(comments)
            else:
                print "no product for add_comments. exception scenario."
        except Exception, e:
            print "add_comments fail! ", e

    def addNewComments(self, comments):
        # if has new comments, we write it to db
        if len(comments) > 0:
            print "new comments ", len(comments)
            sql_insert = "insert into " + self.table_comments + "(productId,commentId,nickname,creationTime,creationTimeStr,score," \
                                                                "userLevelName,userImgFlag,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.executemany(sql_insert, comments)
            self.conn.commit()
            self.split_sentence(comments)
        else:
            print "no new comments"

    # split comment sentences to sub sentences with snownlp.
    def split_sentence(self, comments):
        try:
            subs = []
            # each data format: (productId,commentId,nickname,creationTime,creationTimeStr,score,userLevelName,userImgFlag,content)
            for each in comments:
                pos = len(each)
                items = each[pos - 1].split()  # last one is comment content
                for item in items:
                    s = SnowNLP(item)
                    # split to sub sentences,it will increase recognition probability
                    sens = s.sentences
                    for sentence in sens:
                        s2 = SnowNLP(sentence)
                        # get sentiments of each sentence
                        sentiments = s2.sentiments
                        data = (each[0], each[1], sentence, sentiments)  # 0 productId, 1 commentId
                        subs.append(data)
            print "split_sentence count:", len(subs)
            # write sentence analysis result to sub table
            sql_insert = "insert into " + self.table_comments_sub + "(productId,commentId,sentence,sentiments) " \
                                                                    "values(%s,%s,%s,%s)"
            self.cursor.executemany(sql_insert, subs)
            self.conn.commit()
        except Exception, e:
            print "split_sentence fail! ", e

    # query if comments already exists
    def queryComment(self, commentsId, productId):
        try:
            # check if comments exists
            sql_query = "select COUNT(commentId) from " + self.table_comments + " where productId=" + str(
                productId) + " and commentId=" + str(commentsId)
            self.cursor.execute(sql_query)
            self.conn.commit()
            row = self.cursor.fetchone()
            return row[0]
        except Exception, e:
            print "queryComment fail! ", e
