from twisted.trial import unittest

from mlabsim.main import main


class main_Tests (unittest.TestCase):
    def test_main(self):
        self.assertRaises(NotImplementedError, main)
