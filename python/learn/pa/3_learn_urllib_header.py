#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# learn from Python爬虫入门四之Urllib库的高级用法 http://cuiqingcai.com/954.html

import sys
import urllib
import urllib2


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    url = 'http://www.santostang.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    # values = {'username': 'cqc', 'password': 'XXXX'}
    # data = urllib.urlencode(values)
    # request = urllib2.Request(url, data, headers)
    request = urllib2.Request(url, None, headers)

    try:
        response = urllib2.urlopen(request)
        page = response.read()
        print page
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
    except TypeError, e:
        print e.message


if __name__ == '__main__':
    main()
