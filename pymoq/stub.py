from http import HTTPStatus


class RequestStub(object):
    def __init__(self, url):
        self.url = url

    def can_handle(self, request_handler):
        return self.url == request_handler.path

    def handle_request(self, request_handler):
        request_handler.send_response(HTTPStatus.NO_CONTENT)
        request_handler.end_headers()
