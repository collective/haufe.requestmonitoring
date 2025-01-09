from plone.restapi.services import Service
from time import sleep
class DummyLongRequest(Service):
    def reply(self):
        sleep(30)
        return 'ok'
