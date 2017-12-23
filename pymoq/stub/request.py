from http import HTTPStatus

from pymoq.stub.matcher import MethodMatcher, UrlMatcher


class RequestStub(object):
    def __init__(self, url_pattern, method='GET'):
        self.__matchers = [
            UrlMatcher(url_pattern),
            MethodMatcher(method)
        ]
        self.__response = Response()
        self.method = method.upper()

    def can_handle(self, request_handler):
        return all([matcher.match(request_handler) for matcher in self.__matchers])

    def handle_request(self, request_handler):
        self.__response.send(request_handler)

    def response(self, content, headers=None, http_status=None):
        self.__response = Response(content=content, headers=headers, http_status=http_status)


class Response(object):
    def __init__(self, content=None, headers=None, http_status=None):
        self.__content = content
        self.__headers = {}
        self.__status = http_status

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
        if self.__status is not None:
            return self.__status

        return HTTPStatus.NO_CONTENT if self.__content is None else HTTPStatus.OK
