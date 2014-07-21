"""
This simulates the mlab-ns lookup request, whose code lives here:

https://code.google.com/p/m-lab/source/browse/server/mlabns/handlers/lookup.py?repo=ns

The difference in this module is that we don't support features which
ooni-support does not use and we augment features which ooni-support
would rely on if mlab-ns were to add those features.

Also, this is a twisted web server rather than appengine.
"""


from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


class LookupSimulatorResource (resource.Resource):
    def __init__(self, db):
        # FIXME - db is some simple memory structure holding info;
        # the details will solidfy soon.  This resource reads from
        # this structure.

        resource.Resource.__init__(self)
        self._db = db

    def render_GET(self, request):
        # FIXME: This is not implemented yet.
        request.setResponseCode(500, 'NOT IMPLEMENTED')
        request.finish()
        return NOT_DONE_YET
