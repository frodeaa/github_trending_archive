import glob
import os
import sys
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
)


class Index(object):
    def _archive_paths(self):
        for root, dirs, files in os.walk(archive_dir):
            for f in files:
                if f.endswith(".md"):
                    yield 'archive/%s' % f.replace('.md', '')

    def GET(self):
        paths = reversed(list(self._archive_paths()))
        return render.index(paths)


def main(args):
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    main(sys.argv[1:])
