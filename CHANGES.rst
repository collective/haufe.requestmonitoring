Changelog
=========

0.6.1 (unreleased)
------------------

- Avoid using deprecated zope.app.appsetup and use instead zope.processlifetime.
  [gforcada]

- Include traceback when logging exception

0.6.0 (2021-05-12)
------------------

- Support Zope 4 / Python 3.
  [tschorr]


0.5.1 (2018-04-03)
------------------

- Fix logging format.
  Refs: #9
  [mamico]


0.5.0 (2016-09-29)
------------------

- For all logging output, use unicode and string ``format`` instead of string substitution to avoid possible encoding errors.
  Refs: #5.
  [thet]

- Allow the ``monitorhandler`` define it's zLOG loglevel.
  This makes possible to define the ``ERROR`` level instead of ``WARNING`` for long running requests and get notified by a tool like Sentry, when it's configured to notice ``ERROR`` level logs.
  [thet]

- Remove Logger.py, which is a simpler version of the "Long Request Logger" in DumpTraceback.py and isn't used nor documented.
  [thet]

- Move ``docs/HISTORY.txt`` to ``CHANGES.rst``.
  [thet]

- PEP8 compatibility


0.4.0 (2013-09-20)
------------------

- Added retro-compatibility with old versions of Zope without bein forced to manually patch Zope.
  [giacomos]

- You can now add a ``DISABLE_HAUFE_MONITORING_ON_PDB`` envvar to stop dumping traceback when on Python ``pdb``.
  [keul]


0.3.0 (2012-10-16)
------------------

- Do not use deprecated ``threadframe`` dependency anymore on recent Python versions.
  [keul]

- Fixed egg dependencies for Zope 2.13.
  [keul]

- Added the ``verbosity`` configuration option for the logger.
  [keul]


0.2.3 - (2009/08/11)
--------------------

- Updated documentation.


0.2.2 - (2009/07/20)
--------------------

- Minor cleanup.

- Minor documentation cleanup.


0.2.1 - (2009/05/28)
--------------------

- Configure 'successlogging' by default.

- Slightly updated documentation.


0.2.0 - (2009/05/12)
--------------------

- Initial release.
