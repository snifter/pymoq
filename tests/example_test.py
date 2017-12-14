import unittest

import requests

from pymoq import pymoq


class PyMoqDirectUsageTestCase(unittest.TestCase):

    def test_404_not_found_if_not_configured(self):
        mock = pymoq.Mock()

        urls = [
            'http://localhost:8080/books/',
            'http://localhost:8080/books/2',
            'http://localhost:8080/books/2/chapters',
        ]

        with mock.run():
            for url in urls:
                response = requests.get(url)
                self.assertEqual(response.status_code, 404)

    def test_204_no_content_for_configuration_without_response(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/2/chapters')

        with mock.run():
            response = requests.get('http://localhost:8080/books/2')
            self.assertEqual(response.status_code, 404)

            response = requests.get('http://localhost:8080/books/2/chapters')
            self.assertEqual(response.status_code, 204)

    def test_stub_can_be_configured_with_regex_pattern(self):
        mock = pymoq.Mock()
        mock.create_stub('/books/[0-9]+/chapters')

        with mock.run():
            response = requests.get('http://localhost:8080/books/234/chapters')
            self.assertEqual(response.status_code, 204)
