#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
from lxml import etree


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    raw_cookies='ll="118172"; bid=HLEmDgs6RkI; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1511168413%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DfdWm38HBumU_yKGQoSRMvtFQ4mdr0DsQ13EiH0KFgse%26wd%3D%26eqid%3Df73340030001a4bf000000055a1298a3%22%5D; ps=y; __yadk_uid=T5xwPZtZs9mOy1LAaYoHP1f81qDQqNak; ue="work_man2012@126.com"; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.8cb4=c6dd4936e9be3ae3.1511168413.1.1511169809.1511168413.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.1504003774.1511168415.1511168415.1511168415.1; __utmb=30149280.11.10.1511168415; __utmc=30149280; __utmz=30149280.1511168415.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16991; _ga=GA1.2.1504003774.1511168415; _gid=GA1.2.758825072.1511168867; _gat_UA-7019765-1=1; dbcl2="169919160:UDtl7t4RtFw"'
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
        cookies[key] = value

    user_url='https://www.douban.com/people/169919160/'
    data=requests.get(user_url,cookies=cookies)
    s = etree.HTML(data.text)

    name = s.xpath('//*[@id="db-usr-profile"]/div[2]/h1/text()')
    print(name)

if __name__ == '__main__':
    main()
