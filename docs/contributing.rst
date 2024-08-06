Contributing
============

.. image:: https://jazzband.co/static/img/jazzband.svg
   :target: https://jazzband.co/
   :alt: Jazzband

This is a `Jazzband <https://jazzband.co>`_ project. By contributing you agree
to abide by the `Contributor Code of Conduct <https://jazzband.co/about/conduct>`_
and follow the `guidelines <https://jazzband.co/about/guidelines>`_.

Bug reports and feature requests
--------------------------------

You can report bugs and request features in the `bug tracker
<https://github.com/jazzband/django-debug-toolbar/issues>`_.

Please search the existing database for duplicates before filing an issue.

Code
----

The code is available `on GitHub
<https://github.com/jazzband/django-debug-toolbar>`_. Unfortunately, the
repository contains old and flawed objects, so if you have set
`fetch.fsckObjects
<https://github.com/git/git/blob/0afbf6caa5b16dcfa3074982e5b48e27d452dbbb/Documentation/config.txt#L1381>`_
you'll have to deactivate it for this repository::

    git clone --config fetch.fsckobjects=false https://github.com/jazzband/django-debug-toolbar.git

Once you've obtained a checkout, you should create a virtualenv_ and install
the libraries required for working on the Debug Toolbar::

    $ python -m pip install -r requirements_dev.txt

.. _virtualenv: https://virtualenv.pypa.io/

You can run now run the example application::

    $ DJANGO_SETTINGS_MODULE=example.settings python -m django migrate
    $ DJANGO_SETTINGS_MODULE=example.settings python -m django runserver

For convenience, there's an alias for the second command::

    $ make example

Look at ``example/settings.py`` for running the example with another database
than SQLite.

Architecture
------------

There is high-level information on how the Django Debug Toolbar is structured
in the :doc:`architecture documentation <architecture>`.

Tests
-----

Once you've set up a development environment as explained above, you can run
the test suite for the versions of Django and Python installed in that
environment using the SQLite database::

    $ make test

You can enable coverage measurement during tests::

    $ make coverage

You can also run the test suite on all supported versions of Django and
Python::

    $ tox

This is strongly recommended before committing changes to Python code.

The test suite includes frontend tests written with Selenium. Since they're
annoyingly slow, they're disabled by default. You can run them as follows::

    $ make test_selenium

or by setting the ``DJANGO_SELENIUM_TESTS`` environment variable::

    $ DJANGO_SELENIUM_TESTS=true make test
    $ DJANGO_SELENIUM_TESTS=true make coverage
    $ DJANGO_SELENIUM_TESTS=true tox

Note that by default, ``tox`` enables the Selenium tests for a single test
environment.  To run the entire ``tox`` test suite with all Selenium tests
disabled, run the following::

    $ DJANGO_SELENIUM_TESTS= tox

To test via ``tox`` against other databases, you'll need to create the user,
database and assign the proper permissions. For PostgreSQL in a ``psql``
shell (note this allows the debug_toolbar user the permission to create
databases)::

    psql> CREATE USER debug_toolbar WITH PASSWORD 'debug_toolbar';
    psql> ALTER USER debug_toolbar CREATEDB;
    psql> CREATE DATABASE debug_toolbar;
    psql> GRANT ALL PRIVILEGES ON DATABASE debug_toolbar to debug_toolbar;

For MySQL/MariaDB in a ``mysql`` shell::

    mysql> CREATE DATABASE debug_toolbar;
    mysql> CREATE USER 'debug_toolbar'@'localhost' IDENTIFIED BY 'debug_toolbar';
    mysql> GRANT ALL PRIVILEGES ON debug_toolbar.* TO 'debug_toolbar'@'localhost';
    mysql> GRANT ALL PRIVILEGES ON test_debug_toolbar.* TO 'debug_toolbar'@'localhost';


Style
-----

The Django Debug Toolbar uses `black <https://github.com/psf/black>`__ to
format code and additionally uses ruff. The toolbar uses
`pre-commit <https://pre-commit.com>`__ to automatically apply our style
guidelines when a commit is made. Set up pre-commit before committing with::

    $ pre-commit install

If necessary you can bypass pre-commit locally with::

    $ git commit --no-verify

Note that it runs on CI.

To reformat the code manually use::

    $ pre-commit run --all-files

Patches
-------

Please submit `pull requests
<https://github.com/jazzband/django-debug-toolbar/pulls>`_!

The Debug Toolbar includes a limited but growing test suite. If you fix a bug
or add a feature code, please consider adding proper coverage in the test
suite, especially if it has a chance for a regression.

Translations
------------

Translation efforts are coordinated on `Transifex
<https://www.transifex.com/projects/p/django-debug-toolbar/>`_.

Help translate the Debug Toolbar in your language!

Mailing list
------------

This project doesn't have a mailing list at this time. If you wish to discuss
a topic, please open an issue on GitHub.

Making a release
----------------

Prior to a release, the English ``.po`` file must be updated with ``make
translatable_strings`` and pushed to Transifex. Once translators have done
their job, ``.po`` files must be downloaded with ``make update_translations``.

You will need to
`install the Transifex CLI <https://developers.transifex.com/docs/cli>`_.

To publish a release you have to be a `django-debug-toolbar project lead at
Jazzband <https://jazzband.co/projects/django-debug-toolbar>`__.

The release itself requires the following steps:

#. Update supported Python and Django versions:

   - ``pyproject.toml`` options ``requires-python``, ``dependencies``,
     and ``classifiers``
   - ``README.rst``

   Commit.

#. Update the screenshot in ``README.rst``.

   .. code-block:: console

       $ make example/django-debug-toolbar.png

   Commit.

#. Bump version numbers in ``docs/changes.rst``, ``docs/conf.py``,
   ``README.rst``, and ``debug_toolbar/__init__.py``.
   Add the release date to ``docs/changes.rst``. Commit.

#. Tag the new version.

#. Push the commit and the tag.

#. Publish the release from the Jazzband website.

#. Change the default version of the docs to point to the latest release:
   https://readthedocs.org/dashboard/django-debug-toolbar/versions/
