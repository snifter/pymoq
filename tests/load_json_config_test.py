import unittest
from os import path

import requests

from pymoq import pymoq


class JsonConfigTestCase(unittest.TestCase):
    def test_load_config_from_file(self):
        mock = pymoq.Mock()
        here = path.abspath(path.dirname(__file__))
        path_to_file = path.join(here, 'json', 'test_load_config_from_file.json')
        mock.load(path_to_file)

        with mock.run():
            response = requests.post('http://localhost:8080/books',
                        data={"author": "John Doe", "title": "Lorem ipsum dolor sit amet"})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
            self.assertEqual(response.headers['location'], 'http://localhost:8080/books/1')

            content = response.json()
            self.assertEqual(content['author'], 'John Doe')
            self.assertEqual(content['title'], 'Lorem ipsum dolor sit amet')
            self.assertEqual(content['id'], 1)
