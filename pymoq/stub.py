import re
from http import HTTPStatus


class RequestStub(object):
    def __init__(self, url_pattern):
        self.__url_matcher = UrlMatcher(url_pattern)
        self.__response = Response()

    def can_handle(self, request_handler):
        return self.__url_matcher.match(request_handler.path)

    def handle_request(self, request_handler):
        self.__response.send(request_handler)

    def response(self, content):
        self.__response = Response(content=content)


class Response(object):
    def __init__(self, content=None):
        self.__content = content

    def send(self, request_handler):
        request_handler.send_response(self.status_code)
        if self.__content is not None:
            request_handler.send_header('content-type', 'text/plain; charset=utf-8')
        request_handler.end_headers()

        if self.__content is not None:
            request_handler.wfile.write(bytes(self.__content, 'utf-8'))

    @property
    def status_code(self):
        return HTTPStatus.NO_CONTENT if self.__content is None else HTTPStatus.OK


class UrlMatcher(object):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def match(self, url):
        return self.__re.match(url) is not None
