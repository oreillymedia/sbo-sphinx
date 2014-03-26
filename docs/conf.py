#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sphinx configuration for documentation
"""

from sbo_sphinx.conf import *

project = 'sbo-sphinx'
apidoc_exclude = [
    os.path.join('docs', 'conf.py'),
    os.path.join('sbo_sphinx', 'tests'),
    'setup.py',
    'test_settings.py',
    've',
]
extensions.append('sbo_sphinx.jsdoc')
jsdoc_source_root = os.path.join('..', 'sbo_sphinx', 'jsdoc-toolkit', 'app')
jsdoc_exclude = [os.path.join('app', 'test')]
