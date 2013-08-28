from zope.event import notify
from zope.app.appsetup.interfaces import ProcessStarting
from Zope2.Startup import ZopeStarter
from Zope2.Startup import logger


def wrapped_prepare(self):
    self.orig_prepare()
    logger.info('ZopeStarter patched. Raising IProcessStartingevent.')
    notify(ProcessStarting())

ZopeStarter.orig_prepare = ZopeStarter.prepare
ZopeStarter.prepare = wrapped_prepare
