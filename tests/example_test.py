import unittest

from pymoq import pymoq


class MyTestCase(unittest.TestCase):
    def test_add(self):
        ex = pymoq.Example()
        self.assertEqual(5, ex.add(2, 3))
