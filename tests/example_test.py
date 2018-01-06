import unittest

import requests

from pymoq import pymoq


class ExampleUsageTestCase(unittest.TestCase):
    def test_direct_usage(self):
        content = '{"author": "John Doe", "title": "Lorem ipsum dolor sit amet", "id": 1}'
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'location': 'http://localhost:8090/books/1'
        }

        mock = pymoq.Mock(port=8090)
        mock.create_stub('/books', method='post').response(content,
                                                            headers=headers,
                                                            http_status=201)

        with mock.run():
            response = requests.post('http://localhost:8090/books',
                        data={"author": "John Doe", "title": "Lorem ipsum dolor sit amet"})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
            self.assertEqual(response.headers['location'], 'http://localhost:8090/books/1')
            self.assertEqual(response.text, content)
