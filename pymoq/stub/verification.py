
class RequestLog(object):
    def __init__(self, request_handler):
        self.method = request_handler.command.upper()
        self.url = request_handler.path


class RequestRecorder(object):
    def __init__(self):
        self.__logs = []

    def record(self, request_handler):
        self.__logs.append(RequestLog(request_handler))

    @property
    def count(self):
        return len(self.__logs)
