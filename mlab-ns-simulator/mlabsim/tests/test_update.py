import json

from twisted.trial import unittest
from twisted.web import server

from mock import MagicMock, call

from mlabsim import update

ExampleLookup = """
Example response of production: http://mlab-ns.appspot.com/npad?format=json

{'city': 'Mountain View',
 'country': 'US',
 'fqdn': 'npad.iupui.mlab3.nuq02.measurement-lab.org',
 'ip': ['149.20.5.102', '2001:4F8:1:1001::102'],
 'port': '8001',
 'site': 'nuq02',
 'url': 'http://npad.iupui.mlab3.nuq02.measurement-lab.org:8000'}
"""

class UpdateResourceTests (unittest.TestCase):

    def test_render_PUT_valid_parameters(self):
        # Test data:
        fqdn = 'mlab01.ooni-tests.not-real.except-it-actually-could-be.example.com'

        tool_extra = {
            'collector_onion': 'testfakenotreal.onion',
            }

        expectedentry = {
            'fqdn': fqdn,
            'city': 'Somewheresville',
            'country': 'US',
            'ip': ['127.2.3.4', '::1'],
            'port': 8421,
            'site': 'mlab01',
            'tool_extra': tool_extra
            }

        # Mocks:
        db = {}
        m_request = MagicMock()

        # Fake a request with sufficient parameters:
        # The args are just expectedentry with each value in a single-item list:
        m_request.args = dict( (k, [v]) for (k, v) in expectedentry.iteritems() )

        # Except tool_extra is json encoded:
        m_request.args['tool_extra'] = [json.dumps(tool_extra)]

        # Execute the code under test:
        ur = update.UpdateResource(db)
        retval = ur.render_PUT(m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that m_db now stores fqdn: tool_extra:
        self.assertEqual({fqdn: expectedentry}, db)

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

        expectedentry = {
            'fqdn': fqdn,
            'city': 'Somewheresville',
            'country': 'US',
            'ip': ['127.2.3.4', '::1'],
            'port': 8421,
            'site': 'mlab01',
            'tool_extra': tool_extra
            }

        # Mocks / components:
        m_db = MagicMock()
        m_request = MagicMock()

        # Fake a request with sufficient parameters:
        # The args are just expectedentry with each value in a single-item list:
        m_request.args = dict( (k, [v]) for (k, v) in expectedentry.iteritems() )

        # Except tool_extra is json encoded then mangled with a slice:
        m_request.args['tool_extra'] = [json.dumps(tool_extra)[:-1]]


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
