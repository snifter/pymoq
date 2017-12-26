import unittest
from os import path

import requests

from pymoq import pymoq


class JsonConfigTestCase(unittest.TestCase):

    dir_path = path.join(path.abspath(path.dirname(__file__)), 'json', 'config')

    def test_load_config_from_file(self):
        mock = pymoq.Mock()
        path_to_file = path.join(self.dir_path, 'test_load_config_from_file.json')
        mock.load(path_to_file)

        with mock.run():
            response = requests.post('http://localhost:8080/books',
                                     data={
                                         "author": "John Doe",
                                         "title": "Lorem ipsum dolor sit amet"})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
            self.assertEqual(response.headers['location'], 'http://localhost:8080/books/1')

            content = response.json()
            self.assertEqual(content['author'], 'John Doe')
            self.assertEqual(content['title'], 'Lorem ipsum dolor sit amet')
            self.assertEqual(content['id'], 1)

    def test_content_other_than_json(self):
        mock = pymoq.Mock()
        path_to_file = path.join(self.dir_path, 'test_content_other_than_json.json')
        mock.load(path_to_file)

        with mock.run():
            response = requests.get('http://localhost:8080/books')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, 'Lorem ipsum dolor sit amet')

    def test_content_can_be_empty(self):
        mock = pymoq.Mock()
        path_to_file = path.join(self.dir_path, 'test_content_can_be_empty.json')
        mock.load(path_to_file)

        with mock.run():
            response = requests.get('http://localhost:8080/books')
            self.assertEqual(response.status_code, 204)
