#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    url = 'http://www.server.com/login'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'username': 'cqc', 'password': 'XXXX'}
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    page = response.read()
    print page


if __name__ == '__main__':
    main()
