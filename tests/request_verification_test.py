import unittest

import requests

from pymoq import pymoq


class RequestVerificationTestCase(unittest.TestCase):
    def test_assert_requested_once_not_fails_for_one_request(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books')

        stub.assert_requested_once()

    def test_assert_requested_once_fails_if_no_request(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/1')
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books/1')

        with self.assertRaises(AssertionError):
            stub.assert_requested_once()

    def test_assert_requested_once_fails_if_more_requests(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/1')
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books')
            requests.get('http://localhost:8080/books')

        with self.assertRaises(AssertionError):
            stub.assert_requested_once()
