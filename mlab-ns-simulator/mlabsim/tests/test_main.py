from twisted.trial import unittest

import mock

from mlabsim import main


class main_Tests (unittest.TestCase):

    @mock.patch('logging.basicConfig')
    @mock.patch('twisted.python.log.PythonLoggingObserver')
    def test_main_no_args(self, m_PythonLoggingObserver, m_basicConfig):
        m_reactor = mock.MagicMock()

        main.main([], m_reactor)

        m_reactor.listenTCP.assert_called_with(main.PORT, mock.ANY)
        m_reactor.run.assert_called_with()

