from http import HTTPStatus


class RequestStub(object):
    def __init__(self, url):
        self.url = url

    def can_handle(self, requestHandler):
        return self.url == requestHandler.path

    def handle_request(self, requestHandler):
        requestHandler.send_response(HTTPStatus.NO_CONTENT)
        requestHandler.end_headers()
