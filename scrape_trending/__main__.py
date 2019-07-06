# -*- coding: utf-8 -*-
import sys

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from BeautifulSoup import BeautifulSoup

__attrs = {
    'class': 'col-9 text-gray my-1 pr-4'
}


def trending(content):
    soup = BeautifulSoup(content)
    repoList = soup.find('div', {'class': 'Box'})
    for desc in repoList.findAll('p', __attrs):
        article = desc.parent
        yield (article.h1.a.get('href'),
               article.h1.a.get("href")[1:],
               "".join(desc.text.strip().split('\n')) if desc else '')


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
