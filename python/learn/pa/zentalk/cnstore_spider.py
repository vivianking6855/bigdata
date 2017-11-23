# coding=utf-8
# !/usr/bin/python

# pa zentalk cn store data, with requests + bs4
# data from wandoujia, 华硕的商城, 应用宝
# 百度手机助手（91手机助手）http://shouji.baidu.com/?from=landing
# 华为小米vivo oppo官方商店的评价

import mysql.connector
import time
import WandoujiaSpider
import BaiduSpider

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'zentalk_store',
    'charset': 'utf8'
}

FILE_NAME = 'zentalk.txt'


# 获取当前时间
def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))


def startSpider():
    # spider from wandoujia
    wandoujia_spider = WandoujiaSpider.WandoujiaSpider()
    saveData(wandoujia_spider.start(), "豌豆荚")

    # spider from baidu
    baidu_spider = BaiduSpider.BaiduSpider()
    saveData(baidu_spider.start(), "百度手机助手", True)


def saveData(dict, des, append=False):
    # write to file
    if (append):
        f = open(FILE_NAME, 'a')
    else:
        f = open(FILE_NAME, 'w')
    f.write("\n\n====== " + des + ", " + getCurrentTime() + '====== \n')
    f.write("title: " + dict["title"] + '\n')
    f.write("size: " + dict["size"] + '\n')
    f.write("update: " + dict["update"] + '\n')
    f.write("version: " + dict["version"] + '\n')
    f.write("upload: " + dict["upload"] + '\n')
    f.write("install: " + str(dict["install"]) + '\n')
    f.write("好评率: " + dict["good_eval"] + '\n\n')
    # write comments
    if (dict.has_key("comments")):
        comments = dict["comments"]
        if (len(comments) > 0):
            f.write("用户评论数: " + str(dict["comment_count"]) + '\n')
            for item in comments:
                f.write("评论者: " + item["user"] + '\n')
                f.write("评论时间: " + item["comment_time"] + '\n')
                f.write("评论: " + item["comment_des"] + '\n')
    f.close()


def readData():
    with open(FILE_NAME, 'r') as f:
        print f.read()
        f.close()


def main():
    startSpider()
    readData()


if __name__ == '__main__':
    main()
