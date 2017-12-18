import re
from http import HTTPStatus


class RequestStub(object):
    def __init__(self, url_pattern, method='GET'):
        self.__url_matcher = UrlMatcher(url_pattern)
        self.__response = Response()
        self.__method = method.upper()

    @property
    def method(self):
        return self.__method

    def can_handle(self, request_handler):
        return request_handler.command.upper() == self.__method \
            and self.__url_matcher.match(request_handler.path)

    def handle_request(self, request_handler):
        self.__response.send(request_handler)

    def response(self, content, headers=None):
        self.__response = Response(content=content, headers=headers)


class Response(object):
    def __init__(self, content=None, headers=None):
        self.__content = content
        self.__headers = {}

        if self.__content is not None:
            self.__headers['content-type'] = 'text/plain; charset=utf-8'

        if headers is not None:
            self.__headers.update(headers)

    def send(self, request_handler):
        request_handler.send_response(self.status_code)

        for key, value in self.__headers.items():
            request_handler.send_header(key, value)

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
