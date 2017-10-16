# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

import os

from medikit.events import subscribe

from . import ABSOLUTE_PRIORITY, Feature


class GitFeature(Feature):
    @subscribe('medikit.on_start', priority=ABSOLUTE_PRIORITY)
    def on_start(self, event):
        if not os.path.exists('.git'):
            self.dispatcher.info('git', 'Creating git repository...')
            os.system('git init')
            os.system('git add Projectfile')
            os.system('git commit -m "initial commit"')

    @subscribe('medikit.on_end')
    def on_end(self, event):
        self.render_file_inline(
            '.gitignore', '''
            *.egg-info
            *.iml
            *.pyc
            *.swp
            /.cache
            /.coverage
            /.idea
            /.python*-*
            /build
            /dist
            /htmlcov
            /pylint.html
        ''', event.variables
        )

    @subscribe('medikit.on_file_closed')
    def on_file_change(self, event):
        os.system('git add {}'.format(event.filename))

    @subscribe('medikit.feature.make.on_generate')
    def on_make_generate(self, event):
        event.makefile['VERSION'] = "$(shell git describe 2>/dev/null || echo dev)"


__feature__ = GitFeature