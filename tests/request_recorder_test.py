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
