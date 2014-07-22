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


class UpdateResource (resource.Resource):
    def __init__(self, db):
        """db is a dict which will be modified to map { fqdn -> other_details }"""
        resource.Resource.__init__(self)
        self._db = db

    def render_PUT(self, request):
        [fqdn, tool_extra_json] = self._parse_args(request.args)

        try:
            tool_extra = json.loads(tool_extra_json)
        except ValueError:
            request.setResponseCode(400, 'invalid')
            request.finish()
        else:
            self._db[fqdn] = {'tool_extra': tool_extra}

            request.setResponseCode(200, 'ok')
            request.finish()

        return NOT_DONE_YET

    def _parse_args(self, args):
        for name in ['fqdn', 'tool_extra']:
            [val] = args[name]
            yield val
