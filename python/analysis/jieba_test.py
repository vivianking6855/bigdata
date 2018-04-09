# -*- coding: utf-8 -*-

"""
zenbo nlp 处理类
"""
import re

# sys print config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import uniout

# nlp
import jieba
# 自定义词典
jieba.load_userdict("jieba_dict.txt")
import jieba.analyse
import nltk
import collections

def main():
    list = ["好大一只！",
            "给母亲买的，希望关键时刻，小布可以给独居的老人可以和我们儿女联系上，所以大家都很期待，今天货一到，我立马送去母亲家安装。特把体验发给大家分享：外形和尺寸感觉不错，语音识别度不高，自己找不到回去充电的路径，拍五下后求救功能竟然没用，机器人显示求救信号发出，我手机没有收到任何信号，感觉非常失望",
            "外观很漂亮，京东配送也很好。只是小布语音识别率太低了，而且孩子学习，游戏内容太少，一句话感觉是买了个初级产品。已退货。",
            "很好的小布"]
    topK = 20

    FILE_NAME = 'analysis.txt'
    RESULT_NAME = 'result.txt'
    analysis_file = open(FILE_NAME, 'w')

    for each in list:
        analysis_file.write(each.strip())
    analysis_file.close()

    # analysis
    content = open(FILE_NAME, 'rb').read()
    # 去除文本中的中文符号和英文符号
    content = content.decode("utf8")
    content = re.sub("[\s+\.\!\：\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), content)

    # 1. --- analysis with jieba extract_tags. (word, float)
    data = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)
    with open("result_jieba_tags.txt", 'w') as fw:
        for k, v in data:
            fw.write("%s,%f\n" % (k, v))

    # 2. analysis jieba textrank. (word, float)
    data = jieba.analyse.textrank(content, topK=topK, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    with open("result_jieba_rank.txt", 'w') as fw:
        for k, v in data:
            fw.write("%s,%f\n" % (k, v))

    # 3. --- analysis with jieba & collections. (word, int)
    words_ls = jieba.cut(content)
    data = dict(collections.Counter(words_ls))
    sort_dict = sorted(data.iteritems(), key=lambda d: d[1], reverse=True)
    with open("result_collect.txt", 'w') as fw:
        for k, v in sort_dict:
            fw.write("%s,%d\n" % (k.encode('utf-8'), v))

    # 4. --- analysis with jieba & nltk. (word, int)
    words_ls = jieba.cut(content)
    fd = nltk.FreqDist(words_ls)
    keys = fd.keys()
    item = fd.iteritems()
    dicts = dict(item)
    sort_dict = sorted(dicts.iteritems(), key=lambda d: d[1], reverse=True)
    with open("result_nltk.txt", 'w') as fw:
        for k, v in sort_dict:
            fw.write("%s,%d\n" % (k.encode('utf-8'), v))

if __name__ == '__main__':
    main()
