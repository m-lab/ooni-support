import json

from twisted.trial import unittest
from twisted.web import server

from mock import MagicMock, call

from mlabsim import update


class UpdateResourceTests (unittest.TestCase):

    def test_render_PUT_valid_parameters(self):
        # Test data:
        fqdn = 'mlab01.ooni-tests.not-real.except-it-actually-could-be.example.com'

        tool_extra = {
            'collector_onion': 'testfakenotreal.onion',
            }
        tool_extra_param = json.dumps(tool_extra)

        # Mocks:
        db = {}
        m_request = MagicMock()

        # Fake a request with sufficient parameters:
        m_request.args = {
            'fqdn': [fqdn],
            'tool_extra': [tool_extra_param],
            }

        # Execute the code under test:
        ur = update.UpdateResource(db)
        retval = ur.render_PUT(m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that m_db now stores fqdn: tool_extra:
        self.assertEqual({fqdn: {"tool_extra": tool_extra}}, db)

        # Verify that a 200 response was sent:
        self.assertEqual(
            m_request.mock_calls,
            [call.setResponseCode(200, 'ok'),
             call.finish(),
             ])

    def test_render_PUT_malformed_JSON(self):
        # Test data:
        fqdn = 'mlab01.ooni-tests.not-real.except-it-actually-could-be.example.com'

        tool_extra = {
            'collector_onion': 'testfakenotreal.onion',
            }
        # The slice, [1:] is to mangle the json:
        tool_extra_param = json.dumps(tool_extra)[1:]

        # Mocks / components:
        m_db = MagicMock()
        m_request = MagicMock()

        # Fake a request with sufficient parameters:
        m_request.args = {
            'fqdn': [fqdn],
            'tool_extra': [tool_extra_param],
            }

        # Execute the code under test:
        ur = update.UpdateResource(m_db)
        retval = ur.render_PUT(m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that m_db was not modified (or accessed) in any way:
        self.assertEqual(
            m_db.mock_calls,
            [],
            )

        # Verify that a 400 response was sent:
        self.assertEqual(
            m_request.mock_calls,
            [call.setResponseCode(400, 'invalid'),
             call.finish(),
             ])
