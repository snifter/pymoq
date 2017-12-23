PyMoq
=====
.. image:: https://travis-ci.org/snifter/pymoq.svg?branch=master
    :target: https://travis-ci.org/snifter/pymoq

PyMoq is a tool for mocking HTTP services.


Installation
------------

::

  pip install PyMoq


Usage
-----

By default PyMoq runs on 8080 TCP port, it can be changed:

::

  mock = pymoq.Mock(port=8090)

Stub can be created by setting path and http method (GET is the default).

::

  mock.create_stub('/books', method='post')

It is possible to set path as regex.

::

  mock.create_stub('/books/[0-9]+', method='put')

For each stub a response can be configured with headers and http status code.
Headers has to be dictionary with header name as its key.

::

  mock.create_stub('/books', method='post').response('...',
                                                     headers={'name': 'value'},
                                                     http_status=201)


Example test
^^^^^^^^^^^^
::

  import unittest
  import requests
  from pymoq import pymoq

  class ExampleUsageTestCase(unittest.TestCase):
      def test_direct_usage(self):
        content = '{"author": "John Doe", "title": "Lorem ipsum dolor sit amet", "id": 1}'
        headers = {
          'content-type': 'application/json; charset=utf-8',
          'location': 'http://localhost:8090/books/1'
        }

        mock = pymoq.Mock(port=8090)
        mock.create_stub('/books', method='post').response(content,
                                                          headers=headers,
                                                          http_status=201)

        with mock.run():
            response = requests.post('http://localhost:8090/books',
                              data={"author": "John Doe", "title": "Lorem ipsum dolor sit amet"})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
            self.assertEqual(response.headers['location'], 'http://localhost:8090/books/1')
            self.assertEqual(response.text, content)