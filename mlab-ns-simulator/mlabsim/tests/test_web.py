from twisted.trial import unittest

from mock import patch, call, sentinel

from mlabsim import web


class SiteTests (unittest.TestCase):

    @patch('twisted.web.server.Site.__init__')
    @patch('twisted.web.resource.Resource')
    @patch('mlabsim.lookup.LookupSimulatorResource')
    @patch('mlabsim.update.UpdateResource')
    def test___init__(self, m_UpdateResource, m_LookupSimulatorResource, m_Resource, m_Site__init__):

        site = web.Site()

        self.assertIs(site.requestFactory, web.MlabSimRequest)

        self.assertEqual(
            m_Resource.mock_calls,
            [call(),
             call().putChild('ooni', m_LookupSimulatorResource.return_value),
             call().putChild('update-ooni', m_UpdateResource.return_value),
             ])

        self.assertEqual(
            m_Site__init__.mock_calls,
            [call(site, m_Resource.return_value),
             ])


class MlabSimRequestTests (unittest.TestCase):
    def setUp(self):
        self.req = web.MlabSimRequest(sentinel.ConstructorArg1, sentinel.ConstructorArg2)

    @patch('mlabsim.web.MlabSimRequest._sendStatusAndJsonResponse')
    def test_sendJsonResponse(self, m_ssajr):
        obj = {'fruit', 'banana'}

        self.req.sendJsonResponse(obj)

        m_ssajr.assert_called_with(200, obj)

    @patch('mlabsim.web.MlabSimRequest._sendStatusAndJsonResponse')
    def test_sendJsonError(self, m_ssajr):
        obj = {'fruit', 'banana'}

        self.req.sendJsonError(obj)

        m_ssajr.assert_called_with(400, obj)

    @patch('mlabsim.web.MlabSimRequest._sendStatusAndJsonResponse')
    def test_sendJsonErrorMessage(self, m_ssajr):

        self.req.sendJsonErrorMessage('Boo!')

        m_ssajr.assert_called_with(400, {'error': 'Boo!'})

    @patch('twisted.web.server.Request.setResponseCode')
    @patch('twisted.web.server.Request.setHeader')
    @patch('twisted.web.server.Request.write')
    @patch('twisted.web.server.Request.finish')
    def test__sendStatusAndJsonResponse(self, m_finish, m_write, m_setHeader, m_setResponseCode):
        self.req._sendStatusAndJsonResponse(200, {'fruit': 'banana'})

        m_setResponseCode.assert_called_with(200, 'Ok')
        m_setHeader.assert_called_with('content-type', 'application/json')
        m_write.assert_called_with('{\n  "fruit": "banana"\n}')
        m_finish.assert_called_with()
