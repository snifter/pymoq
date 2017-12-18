import unittest

from pymoq.stub import RequestStub


class HandlerMock(object):
    def __init__(self, path, method):
        self.path = path
        self.command = method


class RequestStubTestCase(unittest.TestCase):
    def test_can_handle_default_method(self):
        target = RequestStub('book/')

        request_handler = HandlerMock('book/', 'GET')
        self.assertTrue(target.can_handle(request_handler))

        request_handler = HandlerMock('book/', 'get')
        self.assertTrue(target.can_handle(request_handler))

    def test_can_handle_defined_method(self):
        target = RequestStub('book/', method='post')

        request_handler = HandlerMock('book/', 'POST')
        self.assertTrue(target.can_handle(request_handler))

        request_handler = HandlerMock('book/', 'post')
        self.assertTrue(target.can_handle(request_handler))

    def test_unable_handle_not_defined_method(self):
        target = RequestStub('book/', method='post')

        request_handler = HandlerMock('book/', 'PUT')
        self.assertFalse(target.can_handle(request_handler))

        request_handler = HandlerMock('book/', 'put')
        self.assertFalse(target.can_handle(request_handler))
