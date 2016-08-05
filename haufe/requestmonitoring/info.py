# -*- coding: utf-8 -*-
"""module to extract (or add) information from a request.

Used mostly as adapters.
"""
from interfaces import IAdditionalInfo
from interfaces import IInfo
from interfaces import ITicket
from thread import allocate_lock
from time import time
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implements
from zope.publisher.interfaces import IRequest


@adapter(IRequest)
@implementer(ITicket)
def get_or_make_ticket(request):
    global _ticket_no
    ticket = getattr(request, '_request_monitoring_ticket_', None)
    if ticket is None:
        _ticket_lock.acquire()
        id = _ticket_no = _ticket_no + 1
        _ticket_lock.release()
        ticket = request._request_monitoring_ticket_ = _Ticket(id)
    return ticket


class _Ticket(object):
    implements(ITicket)

    def __init__(self, id):
        self.id = id
        self.time = time()


_ticket_lock = allocate_lock()
_ticket_no = 0


@adapter(IRequest)
@implementer(IInfo)
def info(request):
    """provide readable information for *request*."""
    qs = request.get('QUERY_STRING')
    aia = IAdditionalInfo(request, None)
    ai = aia and str(aia)
    return (request.get('PATH_INFO', '') + (qs and '?' + qs or '') +
            (ai and (' [%s] ' % ai) or ''))
