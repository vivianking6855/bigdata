# -*- coding: utf-8 -*-
"""
普通工具类
"""

import re
import time
import json
import os


# parse json format file to json object
def readConfigFromFile(path):
    f = open(path)
    cfgs = json.loads(f.read())
    f.close()
    return cfgs

def isFloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

# 获取当前时间
def getCurrentTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 获取当前时间 unix 时间戳
def getCurrentIntTime():
    return (int)(time.mktime(time.localtime(time.time())))

# 字串转化为 unix 时间戳dt为字符串
def dateTimeToInt(dt):
    # 中间过程，一般都需要将字符串转化为时间数组
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

# resolve valid config file path
def resolveProjectPath(path):
    for p in path:
        if os.path.exists(p):
            return p
    print "all config file path are not exsit"

class Tool:
    # 将超链接广告剔除
    removeADLink = re.compile('<div class="link_layer.*?</div>')
    # 去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # 将多行空行删除
    removeNoneLine = re.compile('\n+')

    def replace(self, x):
        x = re.sub(self.removeADLink, "", x)
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeNoneLine, "\n", x)
        # strip()将前后多余内容删除
        return x.strip()

    # it support convert string include unit to count
    # such as 6000,60.2万,1亿
    def getCount(self, x):
        x = self.replace(x)
        if (isFloat(x) or str.isdigit(str(x))):
            return x
        else:
            num = re.findall("\d+\.?\d*", x)[0]
            unit = re.sub(num, "", x)
            unit_number = 1
            if (unit == "万"):
                unit_number = 10000
            elif (unit == "亿"):
                unit_number = 100000000
            return float(num) * unit_number

