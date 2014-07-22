import json
import urllib

from twisted.trial import unittest

import mock

from mlabsim import update


class UpdateResourceTests (unittest.TestCase):

    def test_render_PUT_valid_parameters(self):
        # Test data:
        tool_extra = {
            'collector_onion': 'testfakenotreal.onion',
            }
        tool_extra_param = urllib.quote(json.dumps(tool_extra))

        # Mocks:
        m_db = mock.MagicMock()
        m_request = mock.MagicMock()

        # Fake a request with sufficient parameters:
        m_request.params = {
            'tool_extra': tool_extra_param,
            }

        # Execute the code under test:
        ur = update.UpdateResource(m_db)
        ur.render_PUT(m_request)

        # Verify that m_db now stores tool_extra:
        raise NotImplementedError('verification of m_db storage for tool_extra')



