import os
import unittest
from qotr.config import config

class TestConfig(unittest.TestCase):

    def test_environment(self):
        self.assertEqual(os.environ.get('QOTR_ENV', 'development'),
                         config.name)
