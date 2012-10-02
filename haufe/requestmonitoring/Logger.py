#       $Id: Logger.py,v 1.1.1.1 2005-03-04 10:46:51 dieter Exp $
'''Logging long requests.'''

from zLOG import LOG, WARNING

def factory(config): return handler

def handler(req, handlerState, globalState):
    LOG('RequestMonitor.Logger', WARNING, 'Long running request',
        'Request %s "%s" running in thread %s since %ss' % (
      req.id,
      req.info,
      req.threadId,
      handlerState.monitorTime - req.startTime,
      )
        )
