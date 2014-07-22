"""
This simulates the mlab-ns lookup request, whose code lives here:

https://code.google.com/p/m-lab/source/browse/server/mlabns/handlers/lookup.py?repo=ns

The difference in this module is that we don't support features which
ooni-support does not use and we augment features which ooni-support
would rely on if mlab-ns were to add those features.

Also, this is a twisted web server rather than appengine.
"""

import json

from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


class LookupSimulatorResource (resource.Resource):
    def __init__(self, db):
        """db is a dict mapping { fqdn -> other_stuff }; inserts come from mlabsim.update."""
        resource.Resource.__init__(self)
        self._db = db

    def render_GET(self, request):
        if request.args['match'] == ['all'] and request.args.get('format', ['json']) == ['json']:
            request.setResponseCode(200, 'ok')
            request.write(json.dumps(self._db.values(), indent=2, sort_keys=True))
            request.finish()
        else:
            request.setResponseCode(400, 'invalid')
            request.finish()
        return NOT_DONE_YET
