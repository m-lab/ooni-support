"""
This approximates the mlab-ns slice information gathering.  The actual
system uses nagios and we're not certain about the details.  This much
simplified version is just a web URL anyone may PUT data into.

Warning: This doesn't have any security properties!  We need a way to
prevent the addition of malicious entries.
"""

import logging
import json

from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


DBEntryNames = [
    'city',
    'country',
    'fqdn',
    'ip',
    'port',
    'site',
    'tool_extra',
    ]

class UpdateResource (resource.Resource):
    def __init__(self, db):
        """db is a dict which will be modified to map { fqdn -> other_details }"""
        resource.Resource.__init__(self)
        self._db = db
        self._log = logging.getLogger(type(self).__name__)

    def render_PUT(self, request):
        body = request.content.read()
        self._log.debug('Request body: %r', body)

        try:
            dbentry = json.loads(body)
        except ValueError:
            request.sendJsonErrorMessage('Malformed JSON body.')
            return NOT_DONE_YET

        try:
            fqdn = dbentry['fqdn']
        except KeyError:
            request.sendJsonErrorMessage("Missing 'fqdn' field.")
            return NOT_DONE_YET

        self._db[fqdn] = dbentry

        request.sendJsonResponse('Ok.')
        return NOT_DONE_YET
