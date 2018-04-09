# -*- coding: utf-8 -*-

"""
product 词频分析
"""
import uniout
import sys
import os
import MySQLdb
import re
import jieba
import utils.common as cm
import utils.tool as tool

jieba.load_userdict("../analysis/jieba_dict.txt")  # 自定义词典
import jieba.analyse

# sys print config
reload(sys)
sys.setdefaultencoding('utf-8')

DELETE_TEMP_FILES = True
TOPK = 30  # select top 30 key words


class WordHelp:
    def __init__(self, tables, debug):
        self.table_info = tables[cm.TABLE_INFO_INDEX]
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

            # read sub sentences to file
            file_p = "product_p.txt"  # positive
            file_n = "product_n.txt"  # negative
            words_p = "words_p.txt"  # positive words
            words_n = "words_n.txt"  # negative words
            open(file_p, 'w+').truncate()  # 清空文件内容
            open(file_n, 'w+').truncate()  # 清空文件内容
            for product in products:
                pid = product[0]
                # query positive comments
                query_sql = "select productId,sentence from " + self.table_comments_sub + " where sentiments > 0.8 AND productId=" + pid
                # add query positive comments to file
                self.query_sentence(query_sql, file_p)

                # query negative comments
                query_sql = "select productId,sentence from " + self.table_comments_sub + " where sentiments < 0.3 AND productId=" + pid
                # add query negative comments to file
                self.query_sentence(query_sql, file_n)

                # delete old result if exist
                del_query = "delete from " + self.table_comments_words + " where productId=" + pid
                self.cursor.execute(del_query)
                self.conn.commit()

            # analysis sub sentences
            words_data_p = self.jieba_analysis(file_p, pid, 1)
            words_data_n = self.jieba_analysis(file_n, pid, 0)

            # save analysis words
            self.save_words(words_data_p, words_data_n)

            # delete temp file
            if DELETE_TEMP_FILES:
                os.remove(file_n)
                os.remove(file_p)

        except Exception, e:
            print "analysis fail! ", e

    def query_sentence(self, query_sql, filename):
        self.cursor.execute(query_sql)
        contents = self.cursor.fetchall()
        with open(filename, 'a+') as fw:
            for row in contents:
                sen = row[1]
                fw.write("%s\n" % (sen))

    # analysis with jieba extract_tags. (word, float). sentiments: 0 negative; 1 positive
    def jieba_analysis(self, filename, pid, sentiments):
        content = open(filename, 'rb').read()
        content = content.decode("utf8")
        # 去除文本中的中文符号和英文符号
        content = re.sub("[\s+\.\!\：\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"),
                         "".decode("utf8"), content)
        # 去除数字
        content = re.sub("\d+", "", content)
        data = jieba.analyse.extract_tags(content, topK=TOPK, withWeight=True)
        words_data = []
        for k, v in data:
            word = (pid, k, v, sentiments)
            words_data.append(word)
        return words_data

    # save anaysis words
    def save_words(self, words_data_p, words_data_n):
        # insert result to db
        self.insert_result(words_data_p)
        self.insert_result(words_data_n)

        # write to file, may used for debug
        words_p = "words_p.txt"  # positive words
        words_n = "words_n.txt"  # negative words
        open(words_p, 'w+').truncate()  # 清空文件内容
        open(words_n, 'w+').truncate()  # 清空文件内容
        with open(words_p, 'w+') as fw:
            for row in words_data_p:
                fw.write("[%s, %s]\n" % (row[1], row[2]))
        with open(words_n, 'w+') as fw:
            for row in words_data_n:
                fw.write("[%s, %s]\n" % (row[1], row[2]))
        # delete temp file
        if DELETE_TEMP_FILES:
            os.remove(words_p)
            os.remove(words_n)

    def insert_result(self, words_data):
        # insert result to db
        sql_insert = "insert into " + self.table_comments_words + "(productId,words,weight,sentiments) values(%s,%s,%s,%s)"
        self.cursor.executemany(sql_insert, words_data)
        self.conn.commit()


# enter method
def analysisWords(item, debug):
    cfgjson = tool.readConfigFromFile(".." + os.sep + cm.CONFIGS_PATH + os.sep + item[0])
    configs = cfgjson[cm.CONFIGS][item[1]]
    mysql = WordHelp(configs[cm.TABLES], debug)
    mysql.analysis(configs[cm.PRODUCT_NAME])
