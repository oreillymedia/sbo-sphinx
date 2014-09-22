Setting Up Read the Docs Locally
================================

Installation
------------

`Read the Docs <https://readthedocs.org/>`_ is an open source Django-based web
service for building and hosting Sphinx-based documentation.  The public web
site only supports public code repositories, but a local installation can be
set up to also pull from private repositories.  The site has fairly good
`instructions <http://read-the-docs.readthedocs.org/en/latest/install.html>`_
on how to set up a local installation, but here are a few points to note:

#. Create ``settings/local_settings.py`` - see
   http://read-the-docs.readthedocs.org/en/latest/settings.html for some
   noteworthy options.  You'll probably want to set at least the following::

      DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql_psycopg2',
               'NAME': 'docs',
               'USER': 'postgres',  # or database user of your choice
               'PASSWORD': 'your_password_here',
               'HOST': 'localhost',  # or other database host IP address
               'PORT': '',
           }
       }
       ADMINS = (
           ('Your Name', 'your_username@safaribooksonline.com'),
       )
       ALLOW_PRIVATE_REPOS = True
       CELERY_ALWAYS_EAGER = False

   For a production documentation server, a few a additional settings should
   probably be modified (PRODUCTION_DOMAIN, SLUMBER_PASSWORD, CACHE_BACKEND,
   perhaps the PostgreSQL and/or redis host IP addresses, etc.)

#. Create the database itself (``createdb -U postgres -h localhost -p 5432 -E utf8 -O postgres docs``,
   change the arguments if necessary to match the database settings).

#. Install the PostgreSQL driver for Python::

   pip install psycopg2

#. As of this writing, there's a minor bug in specifying the project's
   database migration dependencies.  To work around this, run the database
   setup commands in the following order::

   ./manage.py syncdb
   ./manage.py migrate projects
   ./manage.py migrate

#. Create a superuser account with the login credentials specified in
   ``SLUMBER_USERNAME`` and ``SLUMBER_PASSWORD`` (test/test by default) via
   ``./manage.py createsuperuser``.

#. If you set the slumber username and password in ``local_settings.py``, you
   shouldn't need to run the ``./manage.py loaddata test_data`` command; other
   than creating a default user for building the documentation in background
   tasks, it just creates some sample documentation project records.

#. Make sure that ``java`` and ``ant`` are installed (these are needed to build
   API documentation for JavaScript code).

Hence the overall sequence ends up looking something like this:

.. code-block:: sh

    git clone https://github.com/rtfd/readthedocs.org.git
    cd readthedocs.org
    virtualenv --python=python2.7 --prompt="(readthedocs)" ve
    . ve/bin/activate
    pip install -r pip_requirements.txt
    cd readthedocs
    # Create settings/local_settings.py
    createdb -U postgres -h localhost -p 5432 -E utf8 -O postgres docs
    pip install pyscopg2
    ./manage.py syncdb
    ./manage.py migrate projects
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver  # in one terminal or as a daemon
    ./manage.py celery worker  # in another terminal or as another daemon

Project Creation
----------------

To create a new project, go to the Dashboard (at http://localhost:8000/dashboard/
by default) and click on :guilabel:`Import`.  Minimally you should set the
name, repo, and description.  The description can usually just be copied from
the GitHub repository.  For a private GitHub repository, the repo entry should
be formatted like ``https://<access_token>:x-oauth-basic@github.com/safarijv/<repo_name>.git``.
See `here <https://help.github.com/articles/creating-an-access-token-for-command-line-use>`_
for documentation on setting up an access token for a GitHub repository (you'll
need permission to modify settings on the repo).

When you click :guilabel:`Create`, it immediately attempts to build the
documentation...and this usually fails.  This is because you now need to click
the :guilabel:`admin` button for the project, go to :guilabel:`Advanced Settings`,
and enable :guilabel:`Use virtualenv`.  Usually you'll also want to set the
:guilabel:`Requirements file` appropriately (usually
``requirements/documentation.txt``.  Click :guilabel:`Submit` to save your
changes, and it should automatically try the build again (if it doesn't, click
on :guilabel:`Build` from the project page.  You should now have a link to
view the HTML documentation for the project.

To rebuild the documentation for the latest version of the code in the ``master``
branch of the repository, just click that :guilabel:`Build` button again.
