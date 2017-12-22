import re


class UrlMatcher(object):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def match(self, request_handler):
        return self.__re.match(request_handler.path) is not None


class MethodMatcher(object):
    def __init__(self, method):
        self.__method = method.upper()

    def match(self, request_handler):
        return request_handler.command.upper() == self.__method
