from contextlib import contextmanager
from http.server import HTTPServer
from threading import Thread

from pymoq.handler import MockRequestHandlerFactory
from pymoq.stub.request import RequestStub


class Mock(object):

    def __init__(self, port=8080):
        self.port = port
        self.stubs = []

    @contextmanager
    def run(self):
        handler_class = MockRequestHandlerFactory(self.stubs).create_handler_class()
        server_address = ('', self.port)
        server = HTTPServer(server_address, handler_class)
        server_thread = ServerThread(server)
        server_thread.start()
        try:
            yield
        finally:
            server_thread.stop()

    def create_stub(self, url, method='GET'):
        stub = RequestStub(url, method=method)
        self.stubs.append(stub)

        return stub


class ServerThread(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
