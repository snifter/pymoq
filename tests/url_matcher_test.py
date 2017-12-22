import unittest

from pymoq.stub.matcher import UrlMatcher


class UrlMatcherTestCase(unittest.TestCase):
    def test_url_equal_pattern(self):
        url = '/books/1'
        self.assertTrue(UrlMatcher(url).match(url))

    def test_url_not_equal_pattern(self):
        pattern = '/authors'
        url = '/books/1'
        self.assertFalse(UrlMatcher(pattern).match(url))

    def test_url_match_pattern(self):
        pattern = '/books/[0-9]+/chapters'
        url = '/books/14/chapters'
        self.assertTrue(UrlMatcher(pattern).match(url))

    def test_url_not_match_pattern(self):
        pattern = '/books/[0-9]+/chapters'
        url = '/books/1e4/chapters'
        self.assertFalse(UrlMatcher(pattern).match(url))
