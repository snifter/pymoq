import unittest

from pymoq.stub.matcher import MethodMatcher


class MethodMatcherTestCase(unittest.TestCase):
    def test_match_defined_method(self):
        target = MethodMatcher('post')
        self.assertTrue(target.match('post'))
        self.assertTrue(target.match('POST'))

        target = MethodMatcher('POST')
        self.assertTrue(target.match('post'))
        self.assertTrue(target.match('POST'))

    def test_not_match_other_method(self):
        target = MethodMatcher('put')
        self.assertFalse(target.match('post'))
        self.assertFalse(target.match('POST'))

        target = MethodMatcher('PUT')
        self.assertFalse(target.match('post'))
        self.assertFalse(target.match('POST'))
