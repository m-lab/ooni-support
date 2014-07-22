"""
This approximates the mlab-ns slice information gathering.  The actual
system uses nagios and we're not certain about the details.  This much
simplified version is just a web URL anyone may PUT data into.

Warning: This doesn't have any security properties!  We need a way to
prevent the addition of malicious entries.
"""

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

    def render_PUT(self, request):
        dbentry = {}

        for name in DBEntryNames:
            # BUG: Multiple values not handled nor tested:
            [value] = request.args[name]
            if name == 'tool_extra':
                try:
                    value = json.loads(value)
                except ValueError:
                    request.setResponseCode(400, 'invalid')
                    request.finish()
                    return NOT_DONE_YET

            dbentry[name] = value

        self._db[dbentry['fqdn']] = dbentry

        request.setResponseCode(200, 'ok')
        request.finish()

        return NOT_DONE_YET
