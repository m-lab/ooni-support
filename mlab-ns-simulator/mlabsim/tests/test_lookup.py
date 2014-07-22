import json

from twisted.trial import unittest
from twisted.web import server

from mock import MagicMock, call

from mlabsim import lookup


class LookupResourceTests (unittest.TestCase):

    def test_render_GET_valid_parameters(self):
        # Test data:
        entries = [
            {
                'fqdn': 'blah',
                'city': 'Somewheresville',
                'country': 'US',
                'ip': ['127.2.3.4', '::1'],
                'port': 8421,
                'site': 'mlab01',
                'tool_extra': {
                    'collector_onion': 'testfakenotreal.onion',
                    },
                },
            {
                'fqdn': 'blorp',
                'city': 'Elsewhereton',
                'country': 'US',
                'ip': ['127.2.3.8', '::7'],
                'port': 1248,
                'site': 'mlab02',
                'tool_extra': {
                    'collector_onion': 'yetanother.onion',
                    },
                },
            ]

        expectedout = json.dumps(entries, indent=2, sort_keys=True)

        # Mocks:
        db = dict( (entry['fqdn'], entry) for entry in entries )
        m_request = MagicMock()

        # Fake a request with sufficient parameters:
        m_request.args = {
            'format': ['json'],
            'match': ['all'],
            }

        # Execute the code under test:
        lsr = lookup.LookupSimulatorResource(db)
        retval = lsr.render_GET(m_request)

        # Verifications:
        self.assertEqual(server.NOT_DONE_YET, retval)

        # Verify that a 200 response was sent:
        self.assertEqual(
            m_request.mock_calls,
            [call.setResponseCode(200, 'ok'),
             call.setHeader('content-type', 'application/json'),
             call.write(expectedout),
             call.finish(),
             ])


    def test_render_GET_bad_args(self):
        vector = [
            ({}, "Missing 'match' parameter."),
            ({'match': ['a', 'b']}, "Multiple 'match' parameters unsupported."),
            ({'match': ['best']}, "Only 'match=all' parameter supported."),
            ({'match': ['all'], 'format': ['a', 'b']}, "Multiple 'format' parameters unsupported."),
            ({'match': ['all'], 'format': ['foo']}, "Only 'format=json' parameter supported."),
            ]

        for (args, errmsg) in vector:
            m_db = MagicMock()
            m_request = MagicMock()
            m_request.args = args

            expectedbody = json.dumps({"error", errmsg}, indent=2, sort_key=True)

            lsr = lookup.LookupSimulatorResource(m_db)
            retval = lsr.render_GET(m_request)

            # Verifications:
            self.assertEqual(server.NOT_DONE_YET, retval)

            # Verify that a 400 response was sent:
            self.assertEqual(
                m_request.mock_calls,
                [call.setResponseCode(400, 'invalid'),
                 call.setHeader('content-type', 'application/json'),
                 call.write(expectedbody),
                 call.finish(),
                 ])

            # Verify that db was not touched:
            self.assertEqual(m_db.mock_calls, [])

