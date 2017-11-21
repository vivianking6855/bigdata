# coding=utf-8
# !/usr/bin/python
# Python中MySQLConnector模块使用方法详解  http://blog.csdn.net/figerdeng/article/details/50493483

import MySQLdb;
import sys

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    conn = MySQLdb.connect(
        host='127.0.0.1',  # 默认127.0.0.1
        port=3306,  # 默认即为3306
        user='root',
        passwd='123456',
        db='zentalk',use_unicode=True)
    cursor = conn.cursor();

    # 获得表中有多少条数据
    list = cursor.execute('select * from summary')
    print list

    # 打印表中的多少数据
    info = cursor.fetchmany(list)
    for unit in info:
        print unit

    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
