Setting Up Read the Docs Locally
================================

Installation
------------

`Read the Docs <https://readthedocs.org/>`_ is an open source Django-based web
service for building and hosting Sphinx-based documentation.  The public web
site only supports public code repositories, but a local installation can be
set up to also pull from private repositories.  The site has fairly good
`instructions <http://read-the-docs.readthedocs.org/en/latest/install.html>`_
on how to set up a local installation, but here are a few recommended changes
and points to note:

#. Before installing its dependencies, edit ``pip_requirements.txt`` to bump
   Sphinx from 1.2 to 1.2.1. This fixes a bug where sphinx-apidoc ignores
   directories to exclude (this can actually cause the build to break as it
   loads files which muck up the options parser for the script itself).

#. Create ``settings/local_settings.py`` - see
   http://read-the-docs.readthedocs.org/en/latest/settings.html for some
   noteworthy options.  You'll probably want to set at least the following::

       SLUMBER_USERNAME = 'your_django_username'
       SLUMBER_PASSWORD = 'your_django_password'
       ADMINS = (
           ('Your Name', 'your_username@safaribooksonline.com'),
       )

#. If you set the slumber username and password in ``local_settings.py``, you
   shouldn't need to run the ``./manage.py loaddata test_data`` command; other
   than creating a default user for building the documentation in background
   tasks, it just creates some sample documentation project records.

Hence the overall sequence ends up looking something like this:

.. code-block:: sh

    git clone https://github.com/rtfd/readthedocs.org.git
    cd readthedocs.org
    virtualenv --python=python2.7 --prompt="(readthedocs)" ve
    . ve/bin/activate
    # Edit pip_requirements.txt to update Sphinx version to 1.2.1
    pip install -r pip_requirements.txt
    cd readthedocs
    # Create settings/local_settings.py
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver

In order to check out code from a private git repository, you'll need to
configure the SSH credentials for the user running the app server.  There
should be a certificate in ``~/.ssh`` with appropriate permissions, as well
as a file at ``~/.ssh/config`` with content like the following::

    Host github.com
        User git
        IdentityFile /Users/username/.ssh/id_rsa

This config file must have the same permissions as the referenced identity
file (read/write for the user, no permissions for anyone else).

Project Creation
----------------

To create a new project, go to the Dashboard (at http://localhost:8000/dashboard/
by default) and click on :guilabel:`Import`.  Minimally you should set the
name, repo, and description.  The description can usually just be copied from
the GitHub repository.  The repo entry should be formatted like
``github.com:safarijv/repo_name.git``.

When you click :guilabel:`Create`, it immediately attempts to build the
documentation...and this usually fails.  This is because you now need to click
the :guilabel:`admin` button for the project, go to :guilabel:`Advanced Settings`,
and enable :guilabel:`Use virtualenv`.  Click :guilabel:`Submit` to save your
changes, and it should automatically try the build again (if it doesn't, click
on :guilabel:`Build` from the project page.  You should now have a link to
view the HTML documentation for the project.

To rebuild the documentation for the latest version of the code in the ``master``
branch of the repository, just click that :guilabel:`Build` button again.
