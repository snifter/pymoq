import unittest

from pymoq.stub.matcher import UrlMatcher
from utils import HandlerMock


class UrlMatcherTestCase(unittest.TestCase):
    def test_url_equal_pattern(self):
        url = '/books/1'
        request_handler = HandlerMock(url, 'GET')

        self.assertTrue(UrlMatcher(url).match(request_handler))

    def test_url_not_equal_pattern(self):
        pattern = '/authors'
        request_handler = HandlerMock('/books/1', 'GET')

        self.assertFalse(UrlMatcher(pattern).match(request_handler))

    def test_url_match_pattern(self):
        pattern = '/books/[0-9]+/chapters'
        request_handler = HandlerMock('/books/14/chapters', 'GET')

        self.assertTrue(UrlMatcher(pattern).match(request_handler))

    def test_url_not_match_pattern(self):
        pattern = '/books/[0-9]+/chapters'
        request_handler = HandlerMock('/books/1e4/chapters', 'GET')

        self.assertFalse(UrlMatcher(pattern).match(request_handler))
