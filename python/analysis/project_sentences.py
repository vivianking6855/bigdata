# -*- coding: utf-8 -*-

"""
product 句子情感分析
"""

import snownlp_sentence as snow

"""each item in array consist of file name(config.json file name) and index (item index in config) 
"""
items = [
    # ("notebook_config.json", 0),
    # ("zenbo_config.json", 0),
    # ("phone_config.json", 0),
    ("compete_config.json", 0)
]

data = [
    "点个赞",
    "屏幕很养眼",
    "非常好用  小米中国最牛的品牌  世界人都选择   做工很精致",
    "绝对值得的一次购物 颜值很高 收到货的时候让我眼前一亮 刚开始用的时候的发热让我担心 但用了鲁大师一调教 后面的散热还是让我比较满意的 不玩游戏40左右的温度 玩游戏的话65左右 算比较可以的 各种硬件规格在这个价位都算顶尖 可以说你想要的都有 绝对超高性价比 毫不夸张的说 是这个价位最值得的选择 唯一有点遗憾的是笔记本关机后第二天再用都会掉7%左右的电 不知道为什么 希望知道的大神可以普及下 我试了下英雄联盟这款游戏 全程最高特效没低于60帧 下面有跑分的附图 大家可以作参考"
]

DEBUG = True


def main():
    #parse_test()
    # parse db comments in config

    index = 0
    for each in items:
        print "parse index:", index, ",", each
        snow.analysisComments(each, DEBUG)
        index = index + 1

def parse_test():
    result = snow.parse_sentence(data)
    for each in result:
        print "index:", each[0], ",sentence:", each[1], ",sentiments", each[2]

main()