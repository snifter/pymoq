from contextlib import contextmanager
from http.server import HTTPServer
from threading import Thread

from pymoq.handler import MockRequestHandlerFactory
from pymoq.stub import RequestStub


class Mock(object):

    port = 8080

    def __init__(self):
        self.stubs = []

    @contextmanager
    def run(self):
        handlerClass = MockRequestHandlerFactory(self.stubs).create_handler_class()
        server_address = ('', self.port)
        server = HTTPServer(server_address, handlerClass)
        serverThread = ServerThread(server)
        serverThread.start()
        try:
            yield
        finally:
            serverThread.stop()

    def create_stub(self, url):
        stub = RequestStub(url)
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
