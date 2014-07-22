import json
import urllib

from twisted.trial import unittest

import mock

from mlabsim import update


class UpdateResourceTests (unittest.TestCase):

    def test_render_PUT_valid_parameters(self):
        # Test data:
        fqdn = 'mlab01.ooni-tests.not-real.except-it-actually-could-be.example.com'

        tool_extra = {
            'collector_onion': 'testfakenotreal.onion',
            }
        tool_extra_param = urllib.quote(json.dumps(tool_extra))

        # Mocks / components:
        db = {}

        # Mocks:
        m_request = mock.MagicMock()

        # Fake a request with sufficient parameters:
        m_request.params = {
            'fqdn': fqdn,
            'tool_extra': tool_extra_param,
            }

        # Execute the code under test:
        ur = update.UpdateResource(db)
        ur.render_PUT(m_request)

        # Verify that m_db now stores fqdn: tool_extra:
        self.assertEqual({fqdn: {"tool_extra": tool_extra}}, db)



