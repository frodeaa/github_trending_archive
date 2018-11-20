# -*- coding: utf-8 -*-
import sys

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from BeautifulSoup import BeautifulSoup

__attrs = {
    'class': lambda x: x and 'd-block' in x.split()
}


def trending(content):
    soup = BeautifulSoup(content)
    for li in soup.findAll('li', __attrs):
        yield (li.div.h3.a.get('href'),
               li.div.h3.a.get("href")[1:],
               "".join(li.p.text.strip().split('\n')) if li.p else '')


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
