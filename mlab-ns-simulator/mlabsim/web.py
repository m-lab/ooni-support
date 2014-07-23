import json

from twisted.web import server, resource

from mlabsim import lookup
from mlabsim import update



class Site (server.Site):
    def __init__(self):
        self.requestFactory = MlabSimRequest

        db = {}

        root = resource.Resource()
        root.putChild('ooni', lookup.LookupSimulatorResource(db))
        root.putChild('update-ooni', update.UpdateResource(db))

        server.Site.__init__(self, root)


class MlabSimRequest (server.Request):

    def sendJsonResponse(self, obj):
        self._sendStatusAndJsonResponse(200, obj)

    def sendJsonError(self, obj):
        self._sendStatusAndJsonResponse(400, obj)

    def sendJsonErrorMessage(self, errmsg):
        self.sendJsonError({'error': errmsg})

    def _sendStatusAndJsonResponse(self, code, doc):
        self.setResponseCode(code, self._StatusCodes[code])
        self.setHeader('content-type', 'application/json')
        self.write(json.dumps(doc, indent=2, sort_keys=True))
        self.finish()

    _StatusCodes = {
        200: 'Ok',
        400: 'Invalid',
        }
