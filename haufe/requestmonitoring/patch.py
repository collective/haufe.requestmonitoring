from zope.event import notify
from zope.app.appsetup.interfaces import ProcessStarting
from Zope2.Startup import ZopeStarter
from Zope2.Startup import logger


def patched_prepare(self):
    self.setupInitialLogging()
    self.setupLocale()
    self.setupSecurityOptions()
    self.setupPublisher()
    # Start ZServer servers before we drop privileges so we can bind to
    # "low" ports:
    self.setupZServer()
    self.setupServers()
    # drop privileges after setting up servers
    self.dropPrivileges()
    self.makeLockFile()
    self.makePidFile()
    self.setupInterpreter()
    self.startZope()
    from App.config import getConfiguration
    config = getConfiguration()
    if not config.twisted_servers:
        self.registerSignals()
    # emit a "ready" message in order to prevent the kinds of emails
    # to the Zope maillist in which people claim that Zope has "frozen"
    # after it has emitted ZServer messages.
    logger.info('Ready to handle requests.*******PATCHED*******')
    self.setupFinalLogging()
    notify(ProcessStarting())

ZopeStarter.prepare = patched_prepare
