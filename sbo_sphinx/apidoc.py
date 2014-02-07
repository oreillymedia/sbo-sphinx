# encoding: utf-8
# Created by Jeremy Bowman at Fri Feb  7 11:47:23 2014
# Copyright (c) 2014 Safari Books Online, LLC. All rights reserved.

"""
Sphinx extension that automatically runs sphinx-apidoc to generate Python API
documentation.  Running it like this instead of as a separate step is
particularly useful when used with Read the Docs (which doesn't really let you
run other shell commands before sphinx-build).  There are a few configuration
options:

* apidoc_source_root - The path relative to conf.py of the root Python package
  for which to generate documentation (default is "..")

* apidoc_output_root - The path relative to conf.py of the directory in which
  to store the generated reST files (default is "python")

* apidoc_exclude - A list of files and directories to omit from the
  documentation (an empty list by default).  Typically used for things like
  conf.py, setup.py and virtualenv directories.  Paths should be relative to
  apidoc_source_root.

The generated files are left in place between builds so they can be inspected.
The output directory should typically be added to .gitignore so the
intermediate files aren't accidentally committed.
"""

import os
from shutil import rmtree
from subprocess import Popen


def generate_docs(app):
    """
    Run sphinx-apidoc to generate Python API documentation for the project.
    """
    config = app.config
    config_dir = app.env.srcdir
    source_root = os.path.join(config_dir, config.apidoc_source_root)
    output_root = os.path.join(config_dir, config.apidoc_output_root)
    execution_dir = os.path.join(config_dir, '..')

    # Remove any files generated by earlier builds
    cleanup(output_root)

    command = ['sphinx-apidoc', '-f', '-o', output_root, source_root]
    # Exclude anything else we were specifically asked to
    for exclude in config.apidoc_exclude:
        command.append(os.path.join(source_root, exclude))
    process = Popen(command, cwd=execution_dir)
    process.wait()


def cleanup(output_root):
    """Remove any reST files which were generated by this extension"""
    if os.path.exists(output_root):
        if os.path.isdir(output_root):
            rmtree(output_root)
        else:
            os.remove(output_root)


def setup(app):
    """Sphinx extension entry point"""
    app.add_config_value('apidoc_exclude', [], 'env')
    app.add_config_value('apidoc_source_root', '..', 'env')
    app.add_config_value('apidoc_output_root', 'python', 'env')
    app.connect('builder-inited', generate_docs)
