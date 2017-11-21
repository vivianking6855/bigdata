#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import bs4

soup = BeautifulSoup(open('index.html'), 'lxml')

# print soup.prettify()
print soup.title
print soup.head
print soup.a
print soup.p.get('class')
print soup.p.string

if type(soup.a.string) == bs4.element.Comment:
    print soup.a.string
