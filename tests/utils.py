class HandlerMock(object):
    def __init__(self, path, method):
        self.path = path
        self.command = method