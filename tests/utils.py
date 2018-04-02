class HandlerMock(object):
    def __init__(self, path, method, headers=None, content=None):
        self.path = path
        self.command = method
        self.headers = headers if headers is not None else dict()

        body = content.encode('utf-8') if content is not None else b''
        self.rfile = ContentReaderMock(body)


class ContentReaderMock(object):
    def __init__(self, content):
        self.content = content

    def read(self, _):
        return self.content
