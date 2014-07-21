"""
This approximates the mlab-ns slice information gathering.  The actual
system uses nagios and we're not certain about the details.  This much
simplified version is just a web URL anyone may PUT data into.

Warning: This doesn't have any security properties!  We need a way to
prevent the addition of malicious entries.
"""


from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


class UpdateResource (resource.Resource):
    def __init__(self, db):
        # FIXME - db is some simple memory structure holding info;
        # the details will solidfy soon.  This resource writes into
        # this structure.

        resource.Resource.__init__(self)
        self._db = db

    def render_PUT(self, request):
        # FIXME: This is not implemented yet.
        request.setResponseCode(500, 'NOT IMPLEMENTED')
        request.finish()
        return NOT_DONE_YET
