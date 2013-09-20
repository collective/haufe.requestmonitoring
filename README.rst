.. contents:: **Table of contents**

Introduction
============

``haufe.requestmonitoring`` implements a detailed request logging functionality
on top of the publication events as introduced with Zope 2.12.


Requirements
============

* Zope 2.12.0b2 or higher
* Currently tested on Zope 2.13.21

You can use this with older Zope releases (2.10.x) but you must also include `ZPublisherEventsBackport`__.

__ http://pypi.python.org/pypi/ZPublisherEventsBackport

Features
========

Fine resolution request logging
-------------------------------

Used as base for ``ztop`` and ``zanalyse``, i.e. helps to determine the Zope load,
detect long running requests and to analyse the causes of restarts.


The implementation in this module registers subscribers for ``IPubStart`` and
``IPubSuccess/IPubFailure``.  For each of these events, a log entry of the form::

   timestamp status request_time type request_id request_info

is written.

Fields
++++++

- *timestamp* is the current time in the format ``%y%m%dT%H%M%S``.

- *status* is ``0`` for ``IPubStart`` events, ``390`` for requests that will
  be retried and the result of ``IStatus`` applied to the response otherwise.

- *request_time* is ``0`` for ``IPubStart`` events. Otherwise, it will be
  the request time in seconds.

- *type* is ``+`` for ``IPubStart`` and ``-`` otherwise.

- *request_id* is the (process) unique request id.

- *request_info* is ``IInfo`` applied to the request.


In addition, a log entry with ``request_info == restarted`` is written when this
logging is activated. Apart from ``request_info`` and ``timestamp`` all other
fields are ``0``. It indicates (obviously) that the server has been restarted.
Following requests get request ids starting with ``1``.

To activate this logging, both ``timelogging.zcml`` must be activated (on by
default) and a ``product-config`` section with name ``timelogging`` must be
defined containing the key ``filebase``.  It specifies the basename of the
logfile; ``.<date>`` will be appended to this base.  Then, ``ITicket``,
``IInfo`` adapters must be defined (e.g.  the one from ``info``).  An
``IStatus`` adapter may be defined for response.

Example::

  <product-config timelogging>
  filebase /path/to/request-logs/instance-foo
  </product-config>


Success request logging
-----------------------

This logging writes two files ``<base>_good.<date>`` and ``<base>_bad.<date>``.
For each request, a character is written to either the good or the bad logfile,
depending on whether the request was successful or unsuccessful. This means,
that only the file size matters for these logfiles.

Usually, response codes >= 500 are considered as unsuccessful requests.  You
can register an ``ISuccessFull`` adapter, when you need a different
classification.

To activate this logging, both ``successlogging.zcml`` must be activated (on by
default) and a ``product-config`` section with name ``successlogging`` must be
defined containing the key ``filebase``.  It specifies the basename of the
logfiles (represented as ``<base>`` above).

Example::

  <product-config successlogging>
  filebase /path/to/request-logs/successful-foo
  </product-config>


Monitoring long running requests
--------------------------------

``haufe.requestmonitoring`` allows you to monitor long-running request. The
following configuration within your ``zope.conf`` configuration file will
install the DumpTracer and check after the ``period`` time passed for requests
running longer than ``time``.

To activate this logging, both ``monitor.zcml`` must be activated (off by
default) and the requestmonitor configuration section must be present::

    zope-conf-additional =
        %import haufe.requestmonitoring
        <requestmonitor requestmonitor>
            # default is 1m
            period 10s
            # default is 1
            verbosity 2
            <monitorhandler dumper>
                factory haufe.RequestMonitoring.DumpTraceback.factory
                # 0 --> no repetition
                repeat -1
                time 10s
            </monitorhandler>
        </requestmonitor>


A typical dump trace looks like this (it shows you the URL and the current 
stacktrace)::


    2009-08-11 14:29:09 INFO Zope Ready to handle requests
    2009-08-11 14:29:09 INFO RequestMonitor started
    2009-08-11 14:29:14 INFO RequestMonitor monitoring 1 requests
    2009-08-11 14:29:19 INFO RequestMonitor monitoring 1 requests
    2009-08-11 14:29:24 INFO RequestMonitor monitoring 1 requests
    2009-08-11 14:29:24 WARNING RequestMonitor.DumpTrace Long running request
    Request 1 "/foo" running in thread -497947728 since 14.9961140156s
    Python call stack (innermost first)
    Module /home/junga/sandboxes/review/parts/instance/Extensions/foo.py, line 4, in foo
    Module Products.ExternalMethod.ExternalMethod, line 231, in __call__
    - __traceback_info__: ((), {}, None)
    Module ZPublisher.Publish, line 46, in call_object
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 126, in publish
    Module ZPublisher.Publish, line 225, in publish_module_standard
    Module ZPublisher.Publish, line 424, in publish_module
    Module Products.ZopeProfiler.ZopeProfiler, line 353, in _profilePublishModule
    Module Products.ZopeProfiler.MonkeyPatcher, line 35, in __call__
    Module ZServer.PubCore.ZServerPublisher, line 28, in __init__

The log line "*RequestMonitor monitoring X requests*" simply says that a request
is under monitor and sometimes you get useless noise in the log file.

You can play with the ``verbosity`` option: put the value to *0* for disable
the log line.
Default value (*1*) will display the log line every time one or more requests
are under monitor.
A value of *2* is more verbose, displaying also info about requests URLs.

Dump trace on pdb
+++++++++++++++++

Traceback dump can became quickly a nightmare if you put a Python debug line on your source code
and then you want to test it running Zope.

In that case you can disable traceback dump when you are executing the debugger. Simply add the
``DISABLE_HAUFE_MONITORING_ON_PDB`` environment variable::

    environment-vars =
        ...
        DISABLE_HAUFE_MONITORING_ON_PDB True

Installation
------------

Add ``haufe.requestmonitoring`` to both ``eggs`` and ``zcml`` option of
your buildout.cfg file.

Author
======

- original author: Dieter Maurer, Haufe Mediengruppe 
- current maintainer: Andreas Jung, Haufe Mediengruppe


License
=======

``haufe.requestmonitoring`` is published under the Zope Public License V 2.1
(ZPL). See LICENSE.txt.


