# coding=utf-8
# !/usr/bin/python
# Python中MySQLConnector模块使用方法详解  http://blog.csdn.net/figerdeng/article/details/50493483

import mysql.connector
import sys

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'zentalk',
    'charset': 'utf8'
}

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    cursor = conn.cursor()
    try:
        sql_query = 'select * from summary;'
        # 获得表中有多少条数据
        list =cursor.execute(sql_query)
        print list
        # 打印表中的多少数据
        info = cursor.fetchmany(list)
        for unit in info:
          print unit
    except mysql.connector.Error as e:
      print('query error!{}'.format(e))
    finally:
        cursor.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    main()
