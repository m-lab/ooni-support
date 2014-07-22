"""
This simulates the mlab-ns lookup request, whose code lives here:

https://code.google.com/p/m-lab/source/browse/server/mlabns/handlers/lookup.py?repo=ns

The difference in this module is that we don't support features which
ooni-support does not use and we augment features which ooni-support
would rely on if mlab-ns were to add those features.

Also, this is a twisted web server rather than appengine.
"""

import logging
import json

from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


class LookupSimulatorResource (resource.Resource):
    def __init__(self, db):
        """db is a dict mapping { fqdn -> other_stuff }; inserts come from mlabsim.update."""
        resource.Resource.__init__(self)
        self._db = db
        self._log = logging.getLogger(type(self).__name__)

    def render_GET(self, request):
        self._log.debug('Request args: %r', request.args)

        try:
            match = self._unpack_arg(request, 'match')
            format = self._unpack_arg(request, 'format', 'json')
            if match != 'all':
                raise BadParameter("Only 'match=all' parameter supported.")
            if format != 'json':
                raise BadParameter("Only 'format=json' parameter supported.")
        except BadParameter, e:
            self._send_response(request, 400, 'invalid', {'error': e.args[0]})
        else:
            self._send_response(request, 200, 'ok', self._db.values())

        return NOT_DONE_YET

    def _unpack_arg(self, request, key, default=None):
        try:
            [value] = request.args[key]
        except KeyError:
            if default is None:
                raise BadParameter('Missing %r parameter.' % (key,))
            else:
                return default
        except ValueError:
            raise BadParameter('Multiple %r parameters unsupported.' % (key,))
        else:
            return value

    def _send_response(self, request, code, status, doc):
        request.setResponseCode(code, status)
        request.setHeader('content-type', 'application/json')
        request.write(json.dumps(doc, indent=2, sort_keys=True))
        request.finish()


class BadParameter (Exception):
    pass
