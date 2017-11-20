#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# learn from http://cuiqingcai.com/947.html

import sys
import urllib2


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    request = urllib2.Request("http://www.baidu.com")
    response = urllib2.urlopen(request)
    print response.read()


if __name__ == '__main__':
    main()
