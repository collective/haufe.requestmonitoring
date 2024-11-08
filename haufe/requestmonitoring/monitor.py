# -*- coding: utf-8 -*-
"""Monitor request execution.

Requires "feature_pubevents".

To activate the monitor, the following preconditions must be met

 * "start_monitor" must be registered as a subscriber

 * The configuration file must have a "<requestmonitor requestmonitor>"
   section with the request monitor configuration.
   See "component.xml" for the schema governing the configuration.

 * "ITicket" and "IInfo" adapters must be registered
   for requests, e.g. the one from "info".
"""

from .interfaces import IInfo
from .interfaces import ITicket
from six.moves._thread import get_ident
from six.moves._thread import start_new_thread
from threading import Lock
from time import sleep
from time import time
import logging
from Zope2.Startup.datatypes import importable_name
from zope.processlifetime import IProcessStarting
from zope.component import adapter
from zope.component import provideHandler
from ZPublisher.interfaces import IPubEnd
from ZPublisher.interfaces import IPubStart


log = logging.getLogger('RequestMonitor')


class Request:
    """request description."""

    def __init__(self, id, info, request, startTime, threadId):
        self.id = id
        self.info = info
        self.request = request
        self.startTime = startTime
        self.threadId = threadId

    def __str__(self):
        return self.request.get('ACTUAL_URL') or '(unknow URL)'


_lock = Lock()
_state = {}


def account_request(request, end):
    ticket = ITicket(request)
    id = ticket.id
    info = str(IInfo(request))
    _lock.acquire()
    try:
        if end:
            del _state[id]
        else:
            _state[id] = Request(id, info, request, ticket.time, get_ident())
    finally:
        _lock.release()


class _Monitor:
    def __init__(self, config):
        self.period = config.period
        self.verbosity = config.verbosity
        self.handlers = [_Handler(hconf, config) for hconf in config.handlers]

    def run(self):
        try:
            log.info('RequestMonitor started')
            while 1:
                sleep(self.period)
                _lock.acquire()
                pending = _state.copy()
                _lock.release()
                if not pending:
                    continue
                monitorTime = time()
                if self.verbosity == 1:
                    log.info('monitoring {0:d} requests'.format(
                        len(pending)))
                elif self.verbosity == 2:
                    log.info(
                        'monitoring {0:d} requests\n{1}'.format(
                            len(pending),
                            u'\n'.join([
                                u'    {0}'.format(req)
                                for req in pending.values()
                            ])
                        )
                    )
                for handler in self.handlers:
                    try:
                        handler(monitorTime, pending)
                    except Exception as e:  # noqa: E722
                        log.exception(
                                'handler exception for {0}: {1}'.format(  # noqa: E501
                                handler.name, e))
        except:  # noqa: E722
            log.exception(
                'monitor thread died with exception')


class _Handler:
    def __init__(self, handlerConfig, monitorConfig):
        self.name = handlerConfig.getSectionName()
        self.time = handlerConfig.time
        self.repeat = handlerConfig.repeat
        self.repeatPeriod = handlerConfig.repeat_period or handlerConfig.time
        self._handler = importable_name(handlerConfig.factory)(handlerConfig)
        self._state = {}  # indexed by threadIds

    def __call__(self, monitorTime, requests):
        for id, req in requests.items():
            threadId = req.threadId
            state = self._state.get(threadId)
            if state is None or state.id != id:
                state = self._state[threadId] = _RequestState(self, id, req)
            state._check(monitorTime, requests)


class _RequestState:
    called = 0  # how often called
    monitorTime = None  # in sec since epoch

    def __init__(self, handler, id, req):
        self._handler = handler
        self._nextTime = req.startTime + handler.time
        self.id = id
        self.request = req

    def _check(self, monitorTime, requests):
        self.monitorTime = monitorTime  # for handlers
        nextTime = self._nextTime
        if nextTime is None or nextTime > monitorTime:
            return
        req = self.request
        handler = self._handler
        handler._handler(req, self, requests)
        self.called += 1
        if handler.repeat >= 0 and self.called > handler.repeat:
            nextTime = None
        else:
            nextTime += handler.repeatPeriod
            # do not allow it to be too far behind
            if nextTime < monitorTime:
                nextTime = monitorTime + 1
        self._nextTime = nextTime


@adapter(IProcessStarting)
def start_monitor(unused):
    """start the request monitor if configured."""
    from App.config import getConfiguration
    config = getConfiguration().product_config.get('requestmonitor')
    if config is None:
        return  # not configured
    # register publication observers
    provideHandler(handle_request_start)
    provideHandler(handle_request_end)
    monitor = _Monitor(config)
    start_new_thread(monitor.run, ())


@adapter(IPubStart)
def handle_request_start(event):
    """handle "IPubStart"."""
    account_request(event.request, False)


@adapter(IPubEnd)
def handle_request_end(event):
    """handle "IPubEnd"."""
    account_request(event.request, True)
