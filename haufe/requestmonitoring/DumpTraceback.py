# -*- coding: utf-8 -*-
'''Dump the traceback of a long running request.'''

from sys import _current_frames as current_frames
from zExceptions.ExceptionFormatter import TextExceptionFormatter

import os
import logging

log = logging.getLogger('RequestMonitor.DumpTrace')


class StackFormatter(TextExceptionFormatter):
    def formatStack(self, stack, limit=None):
        return self.formatException(None, None, _TBFrame(stack), limit)

        # overrides
    def getPrefix(self):
        return 'Python call stack (innermost first)'

    def formatLastLine(self, *unused):
        return ''

    def formatExceptionOnly(self, *unused):
        return
    # Note: "ExtraInfo" often contains references to persistent objects.
    #  We must not touch persistent objects, as we are a foreign thread.
    #  Thus, do not include "ExtraInfo".
    #  ATT: this improves things but it not yet completely safe!

    def formatExtraInfo(self, *unused):
        return


formatter = StackFormatter()


def formatStack(stack, limit=None):
    return formatter.formatStack(stack, limit)


class _NextTBFrame(object):
    '''a delayed next wrapper.'''

    def __get__(self, tbframe, unused):
        back = tbframe.tb_frame.f_back
        if back is not None:
            return _TBFrame(back)


class _TBFrame(object):
    '''a  traceback frame proxy.'''
    tb_next = _NextTBFrame()

    def __init__(self, frame):
        self.tb_frame = frame
        self.tb_lineno = frame.f_lineno  # ATT: might need adjustment!


def factory(config):
    return Handler(config)


class Handler(object):

    def __init__(self, config):
        self.config = config
        self.loglevel = int(getattr(logging, config.loglevel, logging.WARNING))

    def __call__(self, req, handlerState, globalState):
        threadId = req.threadId
        stack_trace = ''.join(formatStack(current_frames()[threadId]))
        if os.environ.get('DISABLE_HAUFE_MONITORING_ON_PDB')\
                and stack_trace.find("  Module pdb,") > -1:
            return
        log.log(
            self.loglevel,
            'Long running request Request {0} "{1}" running in thread {2} since {3}s\n{4}'.format(  # noqa: E501
                req.id,
                req.info,
                threadId,
                handlerState.monitorTime - req.startTime,
                stack_trace,
            )
        )
