# -*- coding: utf-8 -*-

"""
product 词频分析
"""

import jieba_words as jw

"""each item in array consist of file name(config.json file name) and index (item index in config) 
"""
items = [
     #("notebook_config.json", 0),
     ("zenbo_config.json", 0),
    # ("phone_config.json", 0),
    #("compete_config.json", 0)
]

DEBUG = False
index = 0
for it in items:
    print "-------- analysis index:", index, ",", it, "--------"
    jw.analysisWords(it, DEBUG)
    index = index + 1

