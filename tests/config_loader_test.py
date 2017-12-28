import unittest
from os import path

from pymoq.stub.loader import ConfigLoader
from utils import HandlerMock


class ConfigLoaderTestCase(unittest.TestCase):

    dir_path = path.join(path.abspath(path.dirname(__file__)), 'json', 'loader')

    def test_load_all_stubs(self):
        path_to_file = path.join(self.dir_path, 'test_load_all_stubs.json')
        loader = ConfigLoader(path_to_file)
        stubs = loader.load()

        self.assertEqual(len(stubs), 3)

    def test_url_can_be_regex_pattern(self):
        path_to_file = path.join(self.dir_path, 'test_url_can_be_regex_pattern.json')
        loader = ConfigLoader(path_to_file)
        stubs = loader.load()

        stub = stubs[0]

        request_handler = HandlerMock('/books/32/chapters', 'GET')
        self.assertTrue(stub.can_handle(request_handler))

        request_handler = HandlerMock('/books/1/chapters', 'GET')
        self.assertTrue(stub.can_handle(request_handler))

        request_handler = HandlerMock('/books/32', 'GET')
        self.assertFalse(stub.can_handle(request_handler))

    def test_method_can_be_configured(self):
        path_to_file = path.join(self.dir_path, 'test_method_can_be_configured.json')
        loader = ConfigLoader(path_to_file)
        stubs = loader.load()

        stub = stubs[0]

        self.assertEqual(stub.method, 'PUT')

        request_handler = HandlerMock('/books/32', 'PUT')
        self.assertTrue(stub.can_handle(request_handler))
