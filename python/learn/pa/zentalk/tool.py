#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re


# 处理页面标签类
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
    def getCount(self, x, header=None):
        # remove start description string 例如"下载次数：1000万"中的"下载次数："
        if header:
            x = re.sub(header, "", x)

        if (self.isFloat(x) or str.isdigit(str(x))):
            return x
        else:
            num = re.findall("\d+\.?\d*", x)[0]
            unit = re.sub(num, "", x)
            swicher = {
                "万": 10000,
                "亿": 100000000,
            }
            return float(num) * swicher.get(unit, "")

    def isFloat(self, number):
        try:
            num = float(number)
            return True
        except ValueError:
            return False
