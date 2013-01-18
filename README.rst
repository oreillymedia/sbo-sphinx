sbo-sphinx
==========

Overview
--------

Safari Books Online technical documentation is now being written and collected
in a form that can be processed by Sphinx (http://sphinx-doc.org/), a utility
for generating documentation in HTML, PDF, Epub, and other formats from text
files using reST (reStructuredText) wiki markup.  In addition to writing docs
directly, we can have Sphinx grab API documentation from all of our core
programming languages:

* Python docstrings are collected using the sphinx-apidoc command.
* JSDoc-formatted comments in JavaScript are collected using the
  JsDoc Toolkit RST-Template library, which in turn uses jsdoc-toolkit.
* Javadoc comments in Java code are converted into reST files for Sphinx to use
  by the javasphinx extension.

Web service APIs can be documented using httpdomain from sphinx-contrib.

Installation
------------
``pip install -e git://github.com/safarijv/sbo-sphinx.git#egg=sbo-sphinx``

Settings
--------
sbo-sphinx has uses a few Django settings to configure where to look for
its input files and what to do with them:

* ``ROOT_PATH`` - The root directory for the project being documented.  This
  needs to be set when documenting a python project, because this directory
  is added to sys.path in order to import code and retrieve docstrings.
* ``SPHINX_MASTER_DOC`` - Path relative to ``ROOT_PATH`` of the root source
  file for the documentation.  It must be a *.rst file somewhere under
  ``ROOT_PATH``, and the setting must not include the extension.  It should
  usually contain a ``toctree`` directive which lists the top-level documents
  to be included (and those can in turn reference other pages, etc.)
* ``SPHINX_OUTPUT_DIR`` - Path relative to ``ROOT_PATH`` of the directory in
  which to put the generated documentation.  If not specified, defaults to
  ``_build.
* ``SPHINX_PROJECT_NAME`` - The name to be used for the generated set of
  documentation (in titles, headers, etc.)
* ``SPHINX_SHORT_NAME`` - A short name for the project, suitable for use as
  the start of filenames.  If not set, ``SPHINX_PROJECT_NAME`` is used.
* ``SPHINX_PROJECT_VERSION`` - The version number of the project for which
  documentation is being generated.

Usage
-----
To see the list of available commands::

  ./manage.py sphinx

To generate the documentation in a particular target format::

  ./manage.py sphinx <target>

Notes
-----
* The RST-Template library for creating reST files from JSDoc comments
  currently uses jsdoc-toolkit, which is no longer in active development.  If
  we decide that its successor JSDoc 3 has enough useful improvements, I can
  look into updating the library to use that instead.
* In order to be able to include files from anywhere in the project (including
  a README.rst in the root directory to make github happy), the ``conf.py``
  configuration file and ``Makefile`` are copied into the root directory for
  the duration of the Sphinx run; make sure you don't have actual source files
  in those location.

References
----------

* `Sphinx <http://sphinx-doc.org/>`
* `reStructuredText syntax overview <http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`
* `JSDoc <http://code.google.com/p/jsdoc-toolkit/>`
* `JSDoc 3 <http://usejsdoc.org/index.html>`
* `JsDoc Toolkit RST-Template <https://jsdoc-toolkit-rst-template.readthedocs.org/en/latest/index.html>`
* `javasphinx <https://github.com/bronto/javasphinx>`
* `sphinx-contrib <https://bitbucket.org/birkenfeld/sphinx-contrib>` - Lots of
  cool stuff here; support for CoffeeScript, Doxygen, Erlang, Excel, Google
  charts and maps, RESTful HTTP APIs, Ruby, etc.
* `sphinxcontrib.httpdomain <http://packages.python.org/sphinxcontrib-httpdomain/>` - Documenting RESTful HTTP APIs
