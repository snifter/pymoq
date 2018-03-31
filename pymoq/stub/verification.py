
class RequestLog(object):
    def __init__(self, request_handler):
        self.method = request_handler.command.upper()
        self.url = request_handler.path
        self.headers = {item[0].upper(): item[1] for item in request_handler.headers.items()}

    def has_header(self, header, value):
        key = header.upper()
        if key not in self.headers:
            return False

        return self.headers[key] == value


class RequestRecorder(object):
    def __init__(self):
        self.__logs = []

    def record(self, request_handler):
        self.__logs.append(RequestLog(request_handler))

    @property
    def count(self):
        return len(self.__logs)

    def requests_with_header(self, header, value):
        return [log for log in self.__logs if log.has_header(header, value)]
