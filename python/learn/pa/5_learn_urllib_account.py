#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    values = {}
    values['username'] = "1016903103@qq.com"
    values['password'] = "XXXX"
    data = urllib.urlencode(values)
    url = "http://passport.umeng.com/login"
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    print response.read()

if __name__ == '__main__':
    main()