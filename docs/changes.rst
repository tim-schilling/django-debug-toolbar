Change log
==========

Pending
-------

* [i18n] Use correct language in panels

3.8.1 (2022-12-03)
------------------

* Fixed release process by re-adding twine to release dependencies. No
  functional change.

3.8.0 (2022-12-03)
------------------

* Added protection against division by 0 in timer.js
* Auto-update History panel for JavaScript ``fetch`` requests.
* Support `HTMX boosting <https://htmx.org/docs/#boosting/>`__ and
  `Turbo <https://turbo.hotwired.dev/>`__ pages.
* Simplify logic for ``Panel.enabled`` property by checking cookies earlier.
* Include panel scripts in content when ``RENDER_PANELS`` is set to True.
* Create one-time mouseup listener for each mousedown when dragging the
  handle.
* Update package metadata to use Hatchling.
* Fix highlighting on history panel so odd rows are highlighted when
  selected.
* Formalize support for Python 3.11.
* Added TOOLBAR_LANGUAGE setting.

3.7.0 (2022-09-25)
------------------

* Added Profiling panel setting ``PROFILER_THRESHOLD_RATIO`` to give users
  better control over how many function calls are included. A higher value
  will include more data, but increase render time.
* Update Profiling panel to include try to always include user code. This
  code is more important to developers than dependency code.
* Highlight the project function calls in the profiling panel.
* Added Profiling panel setting ``PROFILER_CAPTURE_PROJECT_CODE`` to allow
  users to disable the inclusion of all project code. This will be useful
  to project setups that have dependencies installed under
  ``settings.BASE_DIR``.
* The toolbar's font stack now prefers system UI fonts. Tweaked paddings,
  margins and alignments a bit in the CSS code.
* Only sort the session dictionary when the keys are all strings. Fixes a
  bug that causes the toolbar to crash when non-strings are used as keys.

3.6.0 (2022-08-17)
------------------

* Remove decorator ``signed_data_view`` as it was causing issues with
  `django-urlconfchecks <https://github.com/AliSayyah/django-urlconfchecks/>`__.
* Added pygments to the test environment and fixed a crash when using the
  template panel with Django 4.1 and pygments installed.
* Stayed on top of pre-commit hook and GitHub actions updates.
* Added some workarounds to avoid a Chromium warning which was worrisome to
  developers.
* Avoided using deprecated Selenium methods to find elements.
* Raised the minimum Django version from 3.2 to 3.2.4 so that we can take
  advantage of backported improvements to the cache connection handler.

3.5.0 (2022-06-23)
------------------

* Properly implemented tracking and display of PostgreSQL transactions.
* Removed third party panels which have been archived on GitHub.
* Added Django 4.1b1 to the CI matrix.
* Stopped crashing when ``request.GET`` and ``request.POST`` are neither
  dictionaries nor ``QueryDict`` instances. Using anything but ``QueryDict``
  instances isn't a valid use of Django but, again, django-debug-toolbar
  shouldn't crash.
* Fixed the cache panel to work correctly in the presence of concurrency by
  avoiding the use of signals.
* Reworked the cache panel instrumentation mechanism to monkey patch methods on
  the cache instances directly instead of replacing cache instances with
  wrapper classes.
* Added a :meth:`debug_toolbar.panels.Panel.ready` class method that panels can
  override to perform any initialization or instrumentation that needs to be
  done unconditionally at startup time.
* Added pyflame (for flame graphs) to the list of third-party panels.
* Fixed the cache panel to correctly count cache misses from the get_many()
  cache method.
* Removed some obsolete compatibility code from the stack trace recording code.
* Added a new mechanism for capturing stack traces which includes per-request
  caching to reduce expensive file system operations.  Updated the cache and
  SQL panels to record stack traces using this new mechanism.
* Changed the ``docs`` tox environment to allow passing positional arguments.
  This allows e.g. building a HTML version of the docs using ``tox -e docs
  html``.
* Stayed on top of pre-commit hook updates.
* Replaced ``OrderedDict`` by ``dict`` where possible.

Deprecated features
~~~~~~~~~~~~~~~~~~~

* The ``debug_toolbar.utils.get_stack()`` and
  ``debug_toolbar.utils.tidy_stacktrace()`` functions are deprecated in favor
  of the new ``debug_toolbar.utils.get_stack_trace()`` function.  They will
  removed in the next major version of the Debug Toolbar.

3.4.0 (2022-05-03)
------------------

* Fixed issue of stacktrace having frames that have no path to the file,
  but are instead a string of the code such as
  ``'<frozen importlib._bootstrap>'``.
* Renamed internal SQL tracking context var from ``recording`` to
  ``allow_sql``.

3.3.0 (2022-04-28)
------------------

* Track calls to :py:meth:`django.core.caches.cache.get_or_set`.
* Removed support for Django < 3.2.
* Updated check ``W006`` to look for
  ``django.template.loaders.app_directories.Loader``.
* Reset settings when overridden in tests. Packages or projects using
  django-debug-toolbar can now use Django’s test settings tools, like
  ``@override_settings``, to reconfigure the toolbar during tests.
* Optimize rendering of SQL panel, saving about 30% of its run time.
* New records in history panel will flash green.
* Automatically update History panel on AJAX requests from client.

3.2.4 (2021-12-15)
------------------

* Revert PR 1426 - Fixes issue with SQL parameters having leading and
  trailing characters stripped away.

3.2.3 (2021-12-12)
------------------

* Changed cache monkey-patching for Django 3.2+ to iterate over existing
  caches and patch them individually rather than attempting to patch
  ``django.core.caches`` as a whole. The ``middleware.cache`` is still
  being patched as a whole in order to attempt to catch any cache
  usages before ``enable_instrumentation`` is called.
* Add check ``W006`` to warn that the toolbar is incompatible with
  ``TEMPLATES`` settings configurations with ``APP_DIRS`` set to ``False``.
* Create ``urls`` module and update documentation to no longer require
  importing the toolbar package.


3.2.2 (2021-08-14)
------------------

* Ensured that the handle stays within bounds when resizing the window.
* Disabled ``HistoryPanel`` when ``RENDER_PANELS`` is ``True``
  or if ``RENDER_PANELS`` is ``None`` and the WSGI container is
  running with multiple processes.
* Fixed ``RENDER_PANELS`` functionality so that when ``True`` panels are
  rendered during the request and not loaded asynchronously.
* HistoryPanel now shows status codes of responses.
* Support ``request.urlconf`` override when checking for toolbar requests.


3.2.1 (2021-04-14)
------------------

* Fixed SQL Injection vulnerability, CVE-2021-30459. The toolbar now
  calculates a signature on all fields for the SQL select, explain,
  and analyze forms.
* Changed ``djdt.cookie.set()`` to set ``sameSite=Lax`` by default if
  callers do not provide a value.
* Added ``PRETTIFY_SQL`` configuration option to support controlling
  SQL token grouping. By default it's set to True. When set to False,
  a performance improvement can be seen by the SQL panel.
* Added a JavaScript event when a panel loads of the format
  ``djdt.panel.[PanelId]`` where PanelId is the ``panel_id`` property
  of the panel's Python class. Listening for this event corrects the bug
  in the Timer Panel in which it didn't insert the browser timings
  after switching requests in the History Panel.
* Fixed issue with the toolbar expecting URL paths to start with
  ``/__debug__/`` while the documentation indicates it's not required.

3.2 (2020-12-03)
----------------

* Moved CI to GitHub Actions: https://github.com/jazzband/django-debug-toolbar/actions
* Stopped crashing when ``request.GET`` and ``request.POST`` are
  dictionaries instead of ``QueryDict`` instances. This isn't a valid
  use of Django but django-debug-toolbar shouldn't crash anyway.
* Fixed a crash in the history panel when sending a  JSON POST request
  with invalid JSON.
* Added missing signals to the signals panel by default.
* Documented how to avoid CORS errors now that we're using JavaScript
  modules.
* Verified support for Python 3.9.
* Added a ``css`` and a ``js`` template block to
  ``debug_toolbar/base.html`` to allow overriding CSS and JS.


3.2a1 (2020-10-19)
------------------

* Fixed a regression where the JavaScript code crashed with an invalid
  CSS selector when searching for an element to replace.
* Replaced remaining images with CSS.
* Continued refactoring the HTML and CSS code for simplicity, continued
  improving the use of semantic HTML.
* Stopped caring about prehistoric browsers for good. Started splitting
  up the JavaScript code to take advantage of JavaScript modules.
* Continued removing unused CSS.
* Started running Selenium tests on Travis CI.
* Added a system check which prevents using django-debug-toolbar without
  any enabled panels.
* Added :meth:`Panel.run_checks() <debug_toolbar.panels.Panel.run_checks>` for
  panels to verify the configuration before the application starts.
* Validate the static file paths specified in ``STATICFILES_DIRS``
  exist via :class:`~debug_toolbar.panels.staticfiles.StaticFilesPanel`
* Introduced `prettier <https://prettier.io/>`__ to format the frontend
  code.
* Started accessing history views using GET requests since they do not
  change state on the server.
* Fixed a bug where unsuccessful requests (e.g. network errors) were
  silently ignored.
* Started spellchecking the documentation.
* Removed calls to the deprecated ``request.is_ajax()`` method. These calls
  were unnecessary now that most endpoints return JSON anyway.
* Removed support for Python 3.5.


3.1 (2020-09-21)
----------------

* Fixed a crash in the history panel when sending an empty JSON POST
  request.
* Made ``make example`` also set up the database and a superuser
  account.
* Added a Makefile target for regenerating the django-debug-toolbar
  screenshot.
* Added automatic escaping of panel titles resp. disallowed HTML tags.
* Removed some CSS
* Restructured the SQL stats template.
* Changed command line examples to prefer ``python -m pip`` to ``pip``.


3.0 (2020-09-20)
----------------

* Added an ``.editorconfig`` file specifying indentation rules etc.
* Updated the Italian translation.
* Added support for Django 3.1a1. ``fetch()`` and ``jQuery.ajax`` requests are
  now detected by the absence of a ``Accept: text/html`` header instead of the
  jQuery-specific ``X-Requested-With`` header on Django 3.1 or better.
* Pruned unused CSS and removed hacks for ancient browsers.
* Added the new :attr:`Panel.scripts <debug_toolbar.panels.Panel.scripts>`
  property. This property should return a list of JavaScript resources to be
  loaded in the browser when displaying the panel. Right now, this is used by a
  single panel, the Timer panel. Third party panels can use this property to
  add scripts rather then embedding them in the content HTML.
* Switched from JSHint to ESLint. Added an ESLint job to the Travis CI matrix.
* Debug toolbar state which is only needed in the JavaScript code now uses
  ``localStorage``.
* Updated the code to avoid a few deprecation warnings and resource warnings.
* Started loading JavaScript as ES6 modules.
* Added support for :meth:`cache.touch() <django.core.caches.cache.touch>` when
  using django-debug-toolbar.
* Eliminated more inline CSS.
* Updated ``tox.ini`` and ``Makefile`` to use isort>=5.
* Increased RESULTS_CACHE_SIZE to 25 to better support AJAX requests.
* Fixed the close button CSS by explicitly specifying the
  ``box-sizing`` property.
* Simplified the ``isort`` configuration by taking advantage of isort's
  ``black`` profile.
* Added :class:`~debug_toolbar.panels.history.HistoryPanel` including support
  for AJAX requests.

**Backwards incompatible changes**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Loading panel content no longer executes the scripts elements embedded in the
  HTML. Third party panels that require JavaScript resources should now use the
  :attr:`Panel.scripts <debug_toolbar.panels.Panel.scripts>` property.
* Removed support for end of life Django 1.11. The minimum supported Django is
  now 2.2.
* The Debug Toolbar now loads a `JavaScript module`_. Typical local development
  using Django ``runserver`` is not impacted. However, if your application
  server and static files server are at different origins, you may see CORS
  errors in your browser's development console. See the "Cross-Origin Request
  Blocked" section of the :doc:`installation docs <installation>` for details
  on how to resolve this issue.

.. _JavaScript module: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules

2.2 (2020-01-31)
----------------

* Removed support for end of life Django 2.0 and 2.1.
* Added support for Python 3.8.
* Add locals() option for SQL panel.
* Added support for Django 3.0.


2.1 (2019-11-12)
----------------

* Changed the Travis CI matrix to run style checks first.
* Exposed the ``djdt.init`` function too.
* Small improvements to the code to take advantage of newer Django APIs
  and avoid warnings because of deprecated code.
* Verified compatibility with the upcoming Django 3.0 (at the time of
  writing).


2.0 (2019-06-20)
----------------

* Updated :class:`~debug_toolbar.panels.staticfiles.StaticFilesPanel` to be
  compatible with Django 3.0.
* The :class:`~debug_toolbar.panels.profiling.ProfilingPanel` is now enabled
  but inactive by default.
* Fixed toggling of table rows in the profiling panel UI.
* The :class:`~debug_toolbar.panels.profiling.ProfilingPanel` no longer skips
  remaining panels or middlewares.
* Improved the installation documentation.
* Fixed a possible crash in the template panel.
* Added support for psycopg2 ``Composed`` objects.
* Changed the Jinja2 tests to use Django's own Jinja2 template backend.
* Added instrumentation to queries using server side cursors.
* Too many small improvements and cleanups to list them all.

**Backwards incompatible changes**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Removed support for Python 2.
* Removed support for Django's deprecated ``MIDDLEWARE_CLASSES`` setting.
* Restructured :class:`debug_toolbar.panels.Panel` to execute more like the
  new-style Django MIDDLEWARE. The ``Panel.__init__()`` method is now passed
  ``get_response`` as the first positional argument. The
  :meth:`debug_toolbar.panels.Panel.process_request` method must now always
  return a response. Usually this is the response returned by
  ``get_response()`` but the panel may also return a different response as is
  the case in the :class:`~debug_toolbar.panels.redirects.RedirectsPanel`.
  Third party panels must adjust to this new architecture.
  ``Panel.process_response()`` and ``Panel.process_view()`` have been removed
  as a result of this change.

The deprecated API, ``debug_toolbar.panels.DebugPanel``, has been removed.
Third party panels should use :class:`debug_toolbar.panels.Panel` instead.

The following deprecated settings have been removed:

* ``HIDDEN_STACKTRACE_MODULES``
* ``HIDE_DJANGO_SQL``
* ``INTERCEPT_REDIRECTS``
* ``RESULTS_STORE_SIZE``
* ``ROOT_TAG_ATTRS``
* ``TAG``

1.11 (2018-12-03)
-----------------

* Use ``defer`` on all ``<script>`` tags to avoid blocking HTML parsing,
  removed inline JavaScript.
* Stop inlining images in CSS to avoid Content Security Policy errors
  altogether.
* Reformatted the code using `black <https://github.com/ambv/black>`__.
* Added the Django mail panel to the list of third-party panels.
* Convert system check errors to warnings to accommodate exotic
  configurations.
* Fixed a crash when explaining raw querysets.
* Fixed an obscure Unicode error with binary data fields.
* Added MariaDB and Python 3.7 builds to the CI.

1.10.1 (2018-09-11)
-------------------

* Fixed a problem where the duplicate query detection breaks for
  unhashable query parameters.
* Added support for structured types when recording SQL.
* Made Travis CI also run one test no PostgreSQL.
* Added fallbacks for inline images in CSS.
* Improved cross-browser compatibility around ``URLSearchParams`` usage.
* Fixed a few typos and redundancies in the documentation, removed
  mentions of django-debug-toolbar's jQuery which aren't accurate
  anymore.

1.10 (2018-09-06)
-----------------

* Removed support for Django < 1.11.
* Added support and testing for Django 2.1 and Python 3.7. No actual code
  changes were required.
* Removed the jQuery dependency. This means that django-debug-toolbar
  now requires modern browsers with support for ``fetch``, ``classList``
  etc. The ``JQUERY_URL`` setting is also removed because it isn't
  necessary anymore. If you depend on jQuery, integrate it yourself.
* Added support for the server timing header.
* Added a differentiation between similar and duplicate queries. Similar
  queries are what duplicate queries used to be (same SQL, different
  parameters).
* Stopped hiding frames from Django's contrib apps in stacktraces by
  default.
* Lots of small cleanups and bug fixes.

1.9.1 (2017-11-15)
------------------

* Fix erroneous ``ContentNotRenderedError`` raised by the redirects panel.

1.9 (2017-11-13)
----------------

This version is compatible with Django 2.0 and requires Django 1.8 or
later.

Bug fixes
~~~~~~~~~

* The profiling panel now escapes reported data resulting in valid HTML.
* Many minor cleanups and bug fixes.

1.8 (2017-05-05)
----------------

This version is compatible with Django 1.11 and requires Django 1.8 or
later.

**Backwards incompatible changes**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``debug_toolbar.middleware.show_toolbar`` (the default value of setting
  ``SHOW_TOOLBAR_CALLBACK``) no longer returns ``False`` for AJAX requests.
  This is to allow reusing the ``SHOW_TOOLBAR_CALLBACK`` function to verify
  access to panel views requested via AJAX. Projects defining a custom
  ``SHOW_TOOLBAR_CALLBACK`` should remove checks for AJAX requests in order to
  continue to allow access to these panels.

Features
~~~~~~~~

* New decorator ``debug_toolbar.decorators.require_show_toolbar`` prevents
  unauthorized access to decorated views by checking ``SHOW_TOOLBAR_CALLBACK``
  every request. Unauthorized access results in a 404.
* The ``SKIP_TEMPLATE_PREFIXES`` setting allows skipping templates in
  the templates panel. Template-based form widgets' templates are
  skipped by default to avoid panel sizes going into hundreds of
  megabytes of HTML.

Bug fixes
~~~~~~~~~

* All views are now decorated with
  ``debug_toolbar.decorators.require_show_toolbar`` preventing unauthorized
  access.
* The templates panel now reuses contexts' pretty printed version which
  makes the debug toolbar usable again with Django 1.11's template-based
  forms rendering.
* Long SQL statements are now forcibly wrapped to fit on the screen.

1.7 (2017-03-05)
----------------

Bug fixes
~~~~~~~~~

* Recursive template extension is now understood.
* Deprecation warnings were fixed.
* The SQL panel uses HMAC instead of simple hashes to verify that SQL
  statements have not been changed. Also, the handling of bytes and text
  for hashing has been hardened. Also, a bug with Python's division
  handling has been fixed for improved Python 3 support.
* An error with django-jinja has been fixed.
* A few CSS classes have been prefixed with ``djdt-`` to avoid
  conflicting class names.

1.6 (2016-10-05)
----------------

The debug toolbar was adopted by Jazzband.

Removed features
~~~~~~~~~~~~~~~~

* Support for automatic setup has been removed as it was frequently
  problematic. Installation now requires explicit setup. The
  ``DEBUG_TOOLBAR_PATCH_SETTINGS`` setting has also been removed as it is now
  unused. See the :doc:`installation documentation <installation>` for details.

Bug fixes
~~~~~~~~~

* The ``DebugToolbarMiddleware`` now also supports Django 1.10's ``MIDDLEWARE``
  setting.

1.5 (2016-07-21)
----------------

This version is compatible with Django 1.10 and requires Django 1.8 or later.

Support for Python 3.2 is dropped.

Bug fixes
~~~~~~~~~

* Restore compatibility with sqlparse ≥ 0.2.0.
* Add compatibility with Bootstrap 4, Pure CSS, MDL, etc.
* Improve compatibility with RequireJS / AMD.
* Improve the UI slightly.
* Fix invalid (X)HTML.

1.4 (2015-10-06)
----------------

This version is compatible with Django 1.9 and requires Django 1.7 or later.

New features
~~~~~~~~~~~~

* New panel method :meth:`debug_toolbar.panels.Panel.generate_stats` allows
  panels to only record stats when the toolbar is going to be inserted into
  the response.

Bug fixes
~~~~~~~~~

* Response time for requests of projects with numerous media files has
  been improved.

1.3 (2015-03-10)
----------------

This is the first version compatible with Django 1.8.

New features
~~~~~~~~~~~~

* A new panel is available: Template Profiler.
* The ``SHOW_TOOLBAR_CALLBACK`` accepts a callable.
* The toolbar now provides a :ref:`javascript-api`.

Bug fixes
~~~~~~~~~

* The toolbar handle cannot leave the visible area anymore when the toolbar is
  collapsed.
* The root level logger is preserved.
* The ``RESULTS_CACHE_SIZE`` setting is taken into account.
* CSS classes are prefixed with ``djdt-`` to prevent name conflicts.
* The private copy of jQuery no longer registers as an AMD module on sites
  that load RequireJS.

1.2 (2014-04-25)
----------------

New features
~~~~~~~~~~~~

* The ``JQUERY_URL`` setting defines where the toolbar loads jQuery from.

Bug fixes
~~~~~~~~~

* The toolbar now always loads a private copy of jQuery in order to avoid
  using an incompatible version. It no longer attempts to integrate with AMD.

  This private copy is available in ``djdt.jQuery``. Third-party panels are
  encouraged to use it because it should be as stable as the toolbar itself.

1.1 (2014-04-12)
----------------

This is the first version compatible with Django 1.7.

New features
~~~~~~~~~~~~

* The SQL panel colors queries depending on the stack level.
* The Profiler panel allows configuring the maximum depth.

Bug fixes
~~~~~~~~~

* Support languages where lowercase and uppercase strings may have different
  lengths.
* Allow using cursor as context managers.
* Make the SQL explain more helpful on SQLite.
* Various JavaScript improvements.

Deprecated features
~~~~~~~~~~~~~~~~~~~

* The ``INTERCEPT_REDIRECTS`` setting is superseded by the more generic
  ``DISABLE_PANELS``.

1.0 (2013-12-21)
----------------

This is the first stable version of the Debug Toolbar!

It includes many new features and performance improvements as well a few
backwards-incompatible changes to make the toolbar easier to deploy, use,
extend and maintain in the future.

You're strongly encouraged to review the installation and configuration docs
and redo the setup in your projects.

Third-party panels will need to be updated to work with this version.
