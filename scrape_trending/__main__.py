# -*- coding: utf-8 -*-
import sys

from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(sys.stdin.read())
items = soup.findAll(
    'li', {'class': lambda x: x and 'd-block' in x.split()})

trending = [('https://github.com%s' % li.h3.a.get('href'),
             li.h3.a.get("href")[1:],
             li.p.text.rstrip().lstrip().split("\n")[0] if li.p else '')
            for li in items]

for t in trending:
    print((u'* [%s](%s): %s' % t).rstrip().encode('utf-8'))
