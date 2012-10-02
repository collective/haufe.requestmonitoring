"""Success request logging.

This logging is used by "CheckZope" to determine the amount
of work performed by Zope (in order not to bother it with monitor
probes when it is heavily active) and to detect an unreasonable
error rate.

This logging writes two files "<base>_good.<date>" and "<base>_bad.<date>".
For each request, a character is writen to either the good or
the bad logfile, depending on whether the request was successful or
unsuccessful. This means, that only the file size matters for
these logfiles.

Usually, response codes >= 500 are considered as unsuccessful requests.
You can register an "ISuccessFull" adapter, when you need
a different classification.

To activate this logging, both "successlogging.zcml" must be activated
and a "product-config" section with name "successlogging" must be defined
containing the key "filebase".
It specifies the basename of the logfiles (represented as "<base>" above).
"""

from zope.component import adapter, provideHandler
from zope.app.appsetup.interfaces import IProcessStartingEvent
from ZPublisher.interfaces import IPubSuccess, IPubFailure

from Rotator import Rotator

from interfaces import ISuccessFull, IStatus

_log_good = _log_bad = None


@adapter(IProcessStartingEvent)
def start_successlogging(unused):
    """start successlogging if configured."""
    from App.config import getConfiguration
    config = getConfiguration().product_config.get('successlogging')
    if config is None: return # not configured
    global _log_good, _log_bad
    _log_good = Rotator(config['filebase'] + '_good', lock=True)
    _log_bad = Rotator(config['filebase'] + '_bad', lock=True)
    # register publication observers
    provideHandler(handle_request_success)
    provideHandler(handle_request_failure)
    
    
@adapter(IPubSuccess)
def handle_request_success(event):
    """handle "IPubSuccess"."""
    _log_good.write('*')
    
@adapter(IPubFailure)
def handle_request_failure(event):
    """handle "IPubFailure"."""
    request = event.request
    if event.retry: handle_request_success(event)
    else:
      # Note: Zope forgets (at least sometimes)
      #   to inform the response about the exception.
      #   Work around this bug.
      # When Zope3 views are used for error handling, they no longer
      #   communicate via exceptions with the ZPublisher. Instead, they seem
      #   to use 'setBody' which interferes with the 'exception' call below.
      #   We work around this problem by saving the response state and then
      #   restore it again. Of course, this no longer works around the Zope
      #   bug (forgetting to call 'exception') mentioned above.
        response = request.response
        saved = response.__dict__.copy()
        response.setStatus(event.exc_info[0])
        ok = ISuccessFull(response, None)
        if ok is None:
            status = IStatus(response, None)
            if status is None: status = response.getStatus()
            else: status = int(status)
            ok = status < 500
        if bool(ok): handle_request_success(event)
        else:
            _log_bad.write('*')
        response.__dict__.update(saved) # restore response again
        
