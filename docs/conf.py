# -*- coding: utf-8 -*-

from sbo_sphinx.conf import *

project = 'sbo-sphinx'
apidoc_exclude = [
    os.path.join('docs', 'conf.py'),
    os.path.join('sbo_sphinx', 'management'),
    'setup.py',
    'test_settings.py',
    've',
]
jsdoc_source_root = os.path.join('..', 'sbo_sphinx', 'jsdoc-toolkit', 'app')
jsdoc_exclude = [os.path.join('app', 'test')]