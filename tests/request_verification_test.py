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

    def test_assert_requested_times_not_fails_for_valid_count(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books')
            requests.get('http://localhost:8080/books')

        stub.assert_requested_times(2)

    def test_assert_requested_times_fails_if_not_enough_requests(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books')

        with self.assertRaises(AssertionError):
            stub.assert_requested_times(2)

    def test_assert_requested_times_fails_if_to_many_requests(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books')
            requests.get('http://localhost:8080/books')
            requests.get('http://localhost:8080/books')

        with self.assertRaises(AssertionError):
            stub.assert_requested_times(2)

    def test_assert_requested_with_header_not_fails_if_any_request_had_valid_header(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books', headers={'X-Test': 'false'})
            requests.get('http://localhost:8080/books', headers={'X-Test': 'true'})
            requests.get('http://localhost:8080/books', headers={'X-Test': 'false'})

        stub.assert_requested_with_header('X-Test', 'true')

    def test_assert_requested_with_header_fails_if_no_request_had_valid_header(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books')

        with mock.run():
            requests.get('http://localhost:8080/books', headers={'X-Test': 'false'})
            requests.get('http://localhost:8080/books', headers={'X-Test': 'false'})
            requests.get('http://localhost:8080/books', headers={'X-Test-Other': 'false'})

        with self.assertRaises(AssertionError):
            stub.assert_requested_with_header('X-Test', 'true')

    def test_assert_requested_body_contains_not_fails_if_any_request_contains_content(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books', method='post')

        with mock.run():
            requests.post('http://localhost:8080/books', json={'firstName': 'Wolfgang', 'lastName': 'Mozart'})
            requests.post('http://localhost:8080/books', json={'firstName': 'Jan', 'lastName': 'Bach'})
            requests.post('http://localhost:8080/books', json={'firstName': 'Ludwig', 'lastName': 'Beethoven'})

        stub.assert_requested_body_contains('Bach')

    def test_assert_requested_body_contains_fails_if_no_request_contains_content(self):
        mock = pymoq.Mock()
        stub = mock.create_stub('/books', method='post')

        with mock.run():
            requests.post('http://localhost:8080/books', json={'firstName': 'Wolfgang', 'lastName': 'Mozart'})
            requests.post('http://localhost:8080/books', json={'firstName': 'Jan', 'lastName': 'Bach'})
            requests.post('http://localhost:8080/books', json={'firstName': 'Ludwig', 'lastName': 'Beethoven'})

        with self.assertRaises(AssertionError):
            stub.assert_requested_body_contains('Davies')
