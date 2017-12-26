import json
from codecs import open

from pymoq.stub.request import RequestStub


class ConfigLoader(object):
    def __init__(self, path_to_file):
        self.__path_to_file = path_to_file

    def load(self):
        with open(self.__path_to_file, encoding='utf-8') as fp:
            config = json.load(fp)

        stubs = []

        for item in config:
            stub = self.__create_stub(item)

            if stub is not None:
                stubs.append(stub)

        return stubs

    def __create_stub(self, item):
        if 'request' not in item:
            return None

        request = item['request']
        url = request['url']
        method = request.get('method', 'GET')

        stub = RequestStub(url, method=method)

        if 'response' not in item:
            return stub

        response = item['response']

        content = response['content'] if 'content' in response else None

        if isinstance(content, dict):
            content = json.dumps(response['content'])

        headers = response['headers'] if 'headers' in response else None
        http_status = response['httpStatus'] if 'httpStatus' in response else None

        stub.response(content, headers=headers, http_status=http_status)

        return stub
