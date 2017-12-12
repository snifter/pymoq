import unittest

import requests

from pymoq import pymoq


class PyMoqDirectUsageTestCase(unittest.TestCase):

    def test_404_not_found_if_not_configured(self):
        mock = pymoq.Mock()
        mock.run()

        urls = [
            'http://localhost:8080/books/',
            'http://localhost:8080/books/2',
            'http://localhost:8080/books/2/adnotations',
        ]

        try:
            for url in urls:
                try:
                    response = requests.get(url)
                except Exception as ex:
                    self.fail(ex)

                self.assertEqual(response.status_code, 404)
        finally:
            mock.stop()
