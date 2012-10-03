#       $Id: DumpTraceback.py,v 1.2 2008-01-19 10:34:48 dieter Exp $
'''Dump the traceback of a long running request.'''

try:
    from sys import _current_frames as current_frames
except ImportError:
    # Python 2.4 or lower: use threadframe
    from threadframe import dict as current_frames

from zExceptions.ExceptionFormatter import TextExceptionFormatter
from zLOG import LOG, WARNING

class StackFormatter(TextExceptionFormatter):

    def formatStack(self, stack, limit=None):
        return self.formatException(None, None, _TBFrame(stack), limit)
        
        # overrides
    def getPrefix(self): return 'Python call stack (innermost first)'
    def formatLastLine(self, *unused): return ''
    def formatExceptionOnly(self, *unused): return
    # Note: "ExtraInfo" often contains references to persistent objects.
    #  We must not touch persistent objects, as we are a foreign thread.
    #  Thus, do not include "ExtraInfo".
    #  ATT: this improves things but it not yet completely safe!
    def formatExtraInfo(self, *unused): return
    
formatter = StackFormatter()
def formatStack(stack, limit=None):
    return formatter.formatStack(stack, limit)
    
    
class _NextTBFrame(object):
    '''a delayed next wrapper.'''
    def __get__(self, tbframe, unused):
        back = tbframe.tb_frame.f_back
        if back is not None: return _TBFrame(back)
        
class _TBFrame(object):
    '''a  traceback frame proxy.'''
    tb_next = _NextTBFrame()
    
    def __init__(self, frame):
        self.tb_frame = frame
        self.tb_lineno = frame.f_lineno # ATT: might need adjustment!
        
        
def factory(config): return handler

def handler(req, handlerState, globalState):
    threadId = req.threadId
    LOG('RequestMonitor.DumpTrace', WARNING, 'Long running request',
        'Request %s "%s" running in thread %s since %ss\n%s' % (
      req.id,
      req.info,
      threadId,
      handlerState.monitorTime - req.startTime,
      ''.join(formatStack(current_frames()[threadId])),
      )
        )
    
