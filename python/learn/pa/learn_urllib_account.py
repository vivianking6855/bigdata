#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    values = {"username": "randy_wang@asus.com", "password": "asus@123"}
    data = urllib2.urlencode(values)
    url = "http://passport.umeng.com/login"
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    print response.read()

if __name__ == '__main__':
    main()