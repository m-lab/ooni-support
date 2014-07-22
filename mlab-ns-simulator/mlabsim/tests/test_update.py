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

    def setUp(self):
        # Test data:
        self.fqdn = 'mlab01.ooni-tests.not-real.except-it-actually-could-be.example.com'

        self.expectedentry = {
            'fqdn': self.fqdn,
            'city': 'Somewheresville',
            'country': 'US',
            'ip': ['127.2.3.4', '::1'],
            'port': 8421,
            'site': 'mlab01',
            'tool_extra': {
                'collector_onion': 'testfakenotreal.onion',
                },
            }

        self.entryjson = json.dumps(self.expectedentry, indent=2, sort_keys=True)

        self.m_db = MagicMock()
        self.m_request = MagicMock()

        self.ur = update.UpdateResource(self.m_db)

    def test_render_PUT_valid_parameters(self):
        self.m_request.content.read.return_value = self.entryjson

        # Execute the code under test:
        retval = self.ur.render_PUT(self.m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that m_db now stores the expected entry:
        self.assertEqual(
            self.m_db.mock_calls,
            [call.__setitem__(self.fqdn, self.expectedentry)])

        # Verify that a 200 response was sent:
        self.assertEqual(
            self.m_request.mock_calls,
            [call.content.read(),
             call.setResponseCode(200, 'ok'),
             call.finish(),
             ])

    def test_render_PUT_malformed_JSON(self):
        self.m_request.content.read.return_value = self.entryjson[:-1] # Mangled with slice.

        # Execute the code under test:
        retval = self.ur.render_PUT(self.m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that m_db was not modified (or accessed) in any way:
        self.assertEqual(
            self.m_db.mock_calls,
            [])

        # Verify that a 400 response was sent:
        self.assertEqual(
            self.m_request.mock_calls,
            [call.content.read(),
             call.setResponseCode(400, 'invalid'),
             call.finish(),
             ])
