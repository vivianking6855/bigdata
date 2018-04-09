# -*- coding: utf-8 -*-

"""
snownlp 自然语言处理类 句子情感分析
"""

from snownlp import SnowNLP

import uniout
import sys
import os
import MySQLdb
import utils.common as cm
import utils.tool as tool

# system print config for chinese
reload(sys)
sys.setdefaultencoding('utf-8')


class SentenceHelp:
    def __init__(self, tables, debug):
        self.table_info = tables[cm.TABLE_INFO_INDEX]
        self.table_comments = tables[cm.TABLE_COMMENTS_INDEX]
        self.table_comments_sub = tables[cm.TABLE_COMMENTS_SUB_INDEX]
        self.table_comments_words = tables[cm.TABLE_COMMENTS_WORDS_INDEX]

        if debug:
            self.hosts = '127.0.0.1'  # 本地主机地址
        else:
            self.hosts = '172.29.8.186'  # 数据库主机地址
        print "database:", self.hosts, ",tables:", tables
        self.username = 'root'  # 数据库用户名
        self.password = '123456'  # 数据库密码
        self.database = 'nms'  # 数据库db名字
        self.charsets = 'utf8'
        # connect
        self.connect()

    # connect to mysql db
    def connect(self):
        try:
            self.conn = MySQLdb.connect(host=self.hosts,
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.database,
                                        charset=self.charsets)
            self.cursor = self.conn.cursor()
        except Exception, e:
            print "connect fail! ", e

    def analysis(self, productName):
        try:
            # query products
            product_query = "select productId from " + self.table_info + " where productName=" + "'" + productName + "'"
            self.cursor.execute(product_query)
            products = self.cursor.fetchall()
            # if no product, return
            if not products or len(products) == 0:
                print "can't find product with ", productName
                return

            print "total products [", len(products), "] for productName:", productName
            index = 0
            total_comments = 0
            # query comments
            for product in products:
                productId = product[0]

                # delete old result if exist
                del_query = "delete from " + self.table_comments_sub + " where productId=" + productId
                self.cursor.execute(del_query)
                self.conn.commit()

                # query and parse comments
                query_sql = "select productId,commentId,content from " + self.table_comments + " where productId=" + productId
                self.cursor.execute(query_sql)
                comments = self.cursor.fetchall()

                # index info
                index = index + 1
                total_comments = total_comments + len(comments)

                # if no comments, return
                if not comments or len(comments) == 0:
                    # no comments for this productId
                    continue

                print "index:", index, ", productId:", productId, ", total comments:[", len(comments), "]"
                # parse comments
                subs = parse_comments(comments)
                self.save_sentences(subs)

            print "parsed total comments:[", total_comments, "]"
        except Exception, e:
            print "analysis fail! ", e

    def save_sentences(self, subs):
        try:
            # insert sub comments to sub table
            sql_insert = "insert into " + self.table_comments_sub + "(productId,commentId,sentence,sentiments) " \
                                                                    "values(%s,%s,%s,%s)"
            self.cursor.executemany(sql_insert, subs)
            self.conn.commit()
        except Exception, e:
            print "save_sentences fail! ", e


# split comment sentences to sub sentences with snownlp.
def parse_comments(comments):
    subs = []
    try:
        # each data format: (productId,commentId,content)
        for each in comments:
            items = each[2].split()  # each[2] is comment content
            for item in items:
                s = SnowNLP(item)
                sens = s.sentences
                # split to sub sentences,it will increase recognition probability
                for sentence in sens:
                    s2 = SnowNLP(sentence)
                    # get sentiments of each sentence
                    sentiments = s2.sentiments
                    data = (each[0], each[1], sentence, sentiments)  # 0 productId, 1 commentId
                    subs.append(data)
    except Exception, e:
        print "parse_comments fail! ", e
    return subs


# split comment sentences to sub sentences with snownlp.
def parse_sentence(sentences):
    subs = []
    try:
        index = 0
        for each in sentences:
            items = each.split()
            for item in items:
                s = SnowNLP(item)
                sens = s.sentences
                # split to sub sentence to increase probability
                for sentence in sens:
                    # we must decode to utf-8, other wise sentiments will always 0.5
                    sentence = sentence.decode("utf8")
                    s2 = SnowNLP(sentence)
                    sentiments = s2.sentiments
                    data = (index, sentence, sentiments)  # 0 productId, 1 commentId
                    subs.append(data)
            index = index + 1
    except Exception, e:
        print "parse_sentence fail! ", e
    return subs


# enter method
def analysisComments(item, debug):
    cfgjson = tool.readConfigFromFile(".." + os.sep + cm.CONFIGS_PATH + os.sep + item[0])
    configs = cfgjson[cm.CONFIGS][item[1]]
    mysql = SentenceHelp(configs[cm.TABLES], debug)
    mysql.analysis(configs[cm.PRODUCT_NAME])
