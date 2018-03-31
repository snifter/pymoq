class HandlerMock(object):
    def __init__(self, path, method, headers=None):
        self.path = path
        self.command = method
        self.headers = headers if headers is not None else dict()
