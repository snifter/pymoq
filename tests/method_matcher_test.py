import unittest

from pymoq.stub.matcher import MethodMatcher
from utils import HandlerMock


class MethodMatcherTestCase(unittest.TestCase):
    def test_match_defined_method(self):
        target = MethodMatcher('post')

        request_handler = HandlerMock('/books', 'post')
        self.assertTrue(target.match(request_handler))

        request_handler = HandlerMock('/books', 'POST')
        self.assertTrue(target.match(request_handler))

        target = MethodMatcher('POST')

        request_handler = HandlerMock('/books', 'post')
        self.assertTrue(target.match(request_handler))

        request_handler = HandlerMock('/books', 'POST')
        self.assertTrue(target.match(request_handler))

    def test_not_match_other_method(self):
        target = MethodMatcher('put')

        request_handler = HandlerMock('/books', 'post')
        self.assertFalse(target.match(request_handler))

        request_handler = HandlerMock('/books', 'POST')
        self.assertFalse(target.match(request_handler))

        target = MethodMatcher('PUT')

        request_handler = HandlerMock('/books', 'post')
        self.assertFalse(target.match(request_handler))

        request_handler = HandlerMock('/books', 'POST')
        self.assertFalse(target.match(request_handler))
