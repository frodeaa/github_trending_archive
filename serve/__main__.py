# -*- coding: utf-8 -*-
import codecs
import cStringIO
import datetime
import gzip
import os
import re
import web

t_globals = {
    'datestr': web.datestr
}

module_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(module_dir, 'templates')
archive_dir = os.path.join(os.path.join(
    module_dir, os.path.pardir), 'archive')

gzip_pat = re.compile('^Mozilla/[5,6,7,8,9]|.*MSIE [6,7,8,9].*')

render = web.template.render(template_dir,
                             base='base', globals=t_globals)

urls = (
    '/', 'Index',
    '/archive/(\d\d\d\d-\d\d-\d\d)', 'Archive'
)


def gzip_response(resp):
    resp = str(resp)
    accepts = web.ctx.env.get('HTTP_ACCEPT_ENCODING', None)
    if accepts and accepts.find('gzip') > -1:
        browser = web.ctx.env.get('HTTP_USER_AGENT', None)
        if browser and gzip_pat.match(browser):
            # ok to compress for this browser
            web.webapi.header('Content-Encoding', 'gzip')
            zbuf = cStringIO.StringIO()
            zfile = gzip.GzipFile(mode='wb', fileobj=zbuf,
                                  compresslevel=9)
            zfile.write(resp)
            zfile.close()
            data = zbuf.getvalue()
            web.webapi.header('Content-Length', str(len(data)))
            web.webapi.header('Vary', 'Accept-Encoding', unique=True)
            # don't vary by user-agent, defeats caching
            return data
    return resp


class Index(object):
    def _archive_paths(self):
        l = []
        for root, dirs, files in os.walk(archive_dir):
            for f in files:
                if f.endswith(".md"):
                    l.append('archive/%s' % f.replace('.md', ''))
        list.sort(l)
        l.reverse()
        return l

    def GET(self):
        paths = self._archive_paths()
        date = datetime.datetime.strptime(
            paths[0].split('/')[-1], '%Y-%m-%d')
        web.http.expires(
            (date + datetime.timedelta(days=1)) - datetime.datetime.utcnow())
        web.http.modified(date=date)
        return gzip_response(render.index(paths))


class Archive(object):
    @staticmethod
    def _url(line):
        return re.search('\[([^\]]+)\]\(([^)]+)\)', line)

    @staticmethod
    def _project(m, l):
        return {
            'url': m.group(1),
            'title': m.group(2),
            'description': l[m.end():].strip()
        }

    def _read_archive(self, archive):
        archive_lang = {}
        lang = []
        for line in archive:
            line = line.strip()
            if line.startswith('####'):
                lang = archive_lang[line[4:]] = []
            elif line.startswith('* ['):
                line = line[2:]
                lang.append(self._project(
                    self._url(line), line))
        return archive_lang

    def _next_link_tuple(self, date):
        next_date = date + datetime.timedelta(days=1)
        next_date_str = next_date_str = next_date.strftime('%Y-%m-%d')
        next_link = os.path.join('/archive', next_date_str)
        if next_date.date() >= datetime.datetime.utcnow().date():
            next_date_str = None
        return next_date_str, next_link

    def GET(self, date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        next_date_str, next_link = self._next_link_tuple(date)

        web.http.expires(datetime.timedelta(weeks=100))
        web.http.modified(date=date)
        archive_file = os.path.join(
            archive_dir, date.strftime('%Y-%m'), date_str + '.md'
        )
        with codecs.open(archive_file, 'r',
                         encoding='utf-8') as archive:
            archive_lang = self._read_archive(archive)

        return gzip_response(render.archive(archive_lang.iteritems(),
                                            date_str, next_date_str, next_link))


def main():
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    main()
