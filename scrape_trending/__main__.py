# -*- coding: utf-8 -*-
import sys

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from bs4 import BeautifulSoup


def trending(content):
    soup = BeautifulSoup(content, 'html5lib')
    for article in soup.find_all('article', {'class': 'Box-row'}):
        yield (article.h1.a.get('href'),
               article.h1.a.get('href')[1:],
               ''.join(
                   article.p.text.strip().split('\n')
               ) if article.p else '')


def markdown(trends, lang):
    fmt = u'* [https://github.com%s](%s) %s'
    print((u'\n#### %s' % lang).encode('utf-8'))
    for t in trends:
        print((fmt % t).rstrip().encode('utf-8'))


def main(argv):
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'python:github_trending_archive (by /frodeaa)'
    })
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('https://github.com/trending',
            HTTPAdapter(max_retries=retries))

    for lang in argv:
        url = 'https://github.com/trending?l=%s' % lang
        markdown(trending(s.get(url).text), lang)


if __name__ == '__main__':
    main(sys.argv[1:])
