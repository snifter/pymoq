import unittest

import requests

from pymoq import pymoq


class PyMoqDirectUsageTestCase(unittest.TestCase):

    def test_501_if_not_configured(self):
        mock = pymoq.Mock()

        urls = [
            'http://localhost:8080/books/',
            'http://localhost:8080/books/2',
            'http://localhost:8080/books/2/chapters',
        ]

        with mock.run():
            for url in urls:
                response = requests.get(url)
                self.assertEqual(response.status_code, 501)

    def test_204_no_content_for_configuration_without_response(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/2/chapters')

        with mock.run():
            response = requests.get('http://localhost:8080/books/2/chapters')
            self.assertEqual(response.status_code, 204)

    def test_stub_can_be_configured_with_regex_pattern(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/[0-9]+/chapters')

        with mock.run():
            response = requests.get('http://localhost:8080/books/234/chapters')
            self.assertEqual(response.status_code, 204)

    def test_stub_can_be_configured_with_response_body(self):
        content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

        mock = pymoq.Mock()
        mock.create_stub('/books/2/description').response(content)

        with mock.run():
            response = requests.get('http://localhost:8080/books/2/description')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['content-type'], 'text/plain; charset=utf-8')
            self.assertEqual(response.encoding, 'utf-8')
            self.assertEqual(response.text, content)

    def test_stub_can_be_configured_with_http_status(self):
        mock = pymoq.Mock()
        mock.create_stub('/books').response(None, httpStatus=201)

        with mock.run():
            response = requests.get('http://localhost:8080/books/2/description')
            self.assertEqual(response.status_code, 201)

    def test_stub_can_be_configured_with_response_headers(self):
        content = '{"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}'
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'X-Custom-Header': 'An example'
        }

        mock = pymoq.Mock()
        mock.create_stub('/books/2').response(content, headers=headers)

        with mock.run():
            response = requests.get('http://localhost:8080/books/2')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
            self.assertEqual(response.headers['X-Custom-Header'], 'An example')
            self.assertEqual(response.encoding, 'utf-8')
            self.assertEqual(response.text, content)

    def test_stub_can_be_configured_to_handle_post_method(self):
        mock = pymoq.Mock()
        mock.create_stub('/books', method='post')

        with mock.run():
            response = requests.post('http://localhost:8080/books')
            self.assertEqual(response.status_code, 204)

    def test_stub_can_be_configured_to_handle_put_method(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/1', method='put')

        with mock.run():
            response = requests.put('http://localhost:8080/books/1')
            self.assertEqual(response.status_code, 204)

    def test_stub_can_be_configured_to_handle_delete_method(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/2', method='delete')

        with mock.run():
            response = requests.delete('http://localhost:8080/books/2')
            self.assertEqual(response.status_code, 204)
