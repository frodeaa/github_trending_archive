# -*- coding: utf-8 -*-
import codecs
import datetime
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

render = web.template.render(template_dir,
                             base='base', globals=t_globals)

urls = (
    '/', 'Index',
    '/archive/(\d\d\d\d-\d\d-\d\d)', 'Archive'
)


class Index(object):
    def _archive_paths(self):
        l = []
        for root, dirs, files in os.walk(archive_dir):
            for f in files:
                if f.endswith(".md"):
                    l.append('archive/%s' % f.replace('.md', ''))
        l.reverse()
        return l

    def GET(self):
        paths = self._archive_paths()
        date = datetime.datetime.strptime(
            paths[0].split('/')[-1], '%Y-%m-%d')
        web.http.modified(date=date)
        return render.index(paths)


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

    def GET(self, date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        web.http.modified(date=date)
        archive_file = os.path.join(
            archive_dir, date.strftime('%Y-%m'), date_str + '.md'
        )
        with codecs.open(archive_file, 'r',
                         encoding='utf-8') as archive:
            archive_lang = self._read_archive(archive)
        return render.archive(archive_lang.iteritems())


def main():
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    main()
