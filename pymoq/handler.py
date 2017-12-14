from http import HTTPStatus
from http.server import BaseHTTPRequestHandler


class MockRequestHandlerFactory(object):

    def __init__(self, stubs):
        self.stubs = stubs

    def create_handler_class(self):
        return type('DynamicMockRequestHandler', (MockRequestHandler,), {
            'stubs': lambda x: self.stubs
        })


class MockRequestHandler(BaseHTTPRequestHandler):
    def stubs(self):
        raise NotImplementedError()  # overriden in DynamicMockRequestHandler

    def do_GET(self):
        for stub in self.stubs():
            if stub.can_handle(self):
                stub.handle_request(self)
                return

        self.send_error(HTTPStatus.NOT_FOUND)
