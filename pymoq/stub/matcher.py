import re


class UrlMatcher(object):
    def __init__(self, pattern):
        self.__re = re.compile(pattern)

    def match(self, url):
        return self.__re.match(url) is not None


class MethodMatcher(object):
    def __init__(self, method):
        self.__method = method.upper()

    def match(self, method):
        return method.upper() == self.__method
