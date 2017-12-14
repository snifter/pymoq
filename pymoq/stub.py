import re
from http import HTTPStatus


class RequestStub(object):
    def __init__(self, url_pattern):
        self.__url_matcher = UrlMatcher(url_pattern)

    def can_handle(self, request_handler):
        return self.__url_matcher.match(request_handler.path)

    def handle_request(self, request_handler):
        request_handler.send_response(HTTPStatus.NO_CONTENT)
        request_handler.end_headers()


class UrlMatcher(object):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def match(self, url):
        return self.__re.match(url) is not None
