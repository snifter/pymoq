import unittest

from pymoq.stub.verification import RequestRecorder
from utils import HandlerMock


class RequestRecorderTestCase(unittest.TestCase):
    def test_count_returns_requests_number(self):
        self.__make_count_test(0)
        self.__make_count_test(1)
        self.__make_count_test(3)
        self.__make_count_test(13)

    def __make_count_test(self, count):
        request_handler = HandlerMock('/books/32', 'GET')

        target = RequestRecorder()
        for _ in range(count):
            target.record(request_handler)

        self.assertEqual(count, target.count)

    def test_requests_with_header_returns_filtered_requests(self):
        target = RequestRecorder()

        target.record(HandlerMock('/books/30', 'GET'))
        target.record(HandlerMock('/books/31', 'GET', headers={'X-Test': 'valid'}))
        target.record(HandlerMock('/books/32', 'GET', headers={'X-Test': 'invalid'}))
        target.record(HandlerMock('/books/33', 'GET', headers={'X-Test-Other': 'valid'}))

        actual = target.requests_with_header('X-Test', 'valid')

        self.assertEqual(1, len(actual))
        self.assertEqual('/books/31', actual[0].url)

    def test_requests_with_content_returns_filtered_requests(self):
        target = RequestRecorder()

        target.record(HandlerMock('/books/30', 'POST'))
        target.record(HandlerMock('/books/31', 'POST', content='Author: Hemingway'))
        target.record(HandlerMock('/books/32', 'POST', content='Author: Dickens'))
        target.record(HandlerMock('/books/33', 'POST', content='Author: Proust'))

        actual = target.requests_with_content('Dickens')

        self.assertEqual(1, len(actual))
        self.assertEqual('/books/32', actual[0].url)
