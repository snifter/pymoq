from http import HTTPStatus
from http.server import BaseHTTPRequestHandler


class MockRequestHandlerFactory(object):

    def __init__(self, stubs):
        self.stubs = stubs

    def create_handler_class(self):
        methodsDict = {
            'stubs': lambda x: self.stubs
        }

        for stub in self.stubs:
            key = 'do_{method}'.format(method=stub.method)
            if key not in methodsDict:
                methodsDict[key] = lambda x: x.handleRequest()

        return type('DynamicMockRequestHandler', (MockRequestHandler,), methodsDict)


class MockRequestHandler(BaseHTTPRequestHandler):
    def stubs(self):
        raise NotImplementedError()  # overriden in DynamicMockRequestHandler

    def handleRequest(self):
        for stub in self.stubs():
            if stub.can_handle(self):
                stub.handle_request(self)
                return

        self.send_error(HTTPStatus.NOT_IMPLEMENTED, 'No stub found to handle request')
