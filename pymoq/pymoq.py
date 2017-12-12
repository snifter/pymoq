from contextlib import contextmanager
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class Mock(object):

    port = 8080

    def __init__(self):
        server_address = ('', self.port)
        server = HTTPServer(server_address, MockRequestHandler)
        self.serverThread = ServerThread(server)

    @contextmanager
    def run(self):
        self.serverThread.start()
        try:
            yield
        finally:
            self.serverThread.stop()


class MockRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_error(HTTPStatus.NOT_FOUND)


class ServerThread(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
