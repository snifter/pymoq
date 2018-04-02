PyMoq
=====
.. image:: https://travis-ci.org/snifter/pymoq.svg?branch=0.3.0
    :target: https://travis-ci.org/snifter/pymoq

.. image:: https://codecov.io/gh/snifter/pymoq/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/snifter/pymoq

.. image:: https://img.shields.io/github/issues/snifter/pymoq.svg?style=flat
    :target: https://github.com/snifter/pymoq/issues

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

Configure with JSON file
------------------------

A mock can be configured with json file. A file should looks like:

::

  [{
      "request": {
          "url": "/books",
          "method": "post"
      },
      "response": {
          "content": {"author": "John Doe", "title": "Lorem ipsum dolor sit amet", "id": 1},
          "headers": {
              "content-type": "application/json; charset=utf-8",
              "location": "http://localhost:8080/books/1"
          },
          "httpStatus": 201
      }
  }]

Example test
^^^^^^^^^^^^
::

  import unittest
  import requests
  from pymoq import pymoq


  class JsonConfigTestCase(unittest.TestCase):
      def test_load_config_from_file(self):
          mock = pymoq.Mock()
          mock.load('config.json')

          with mock.run():
              response = requests.post('http://localhost:8080/books',
                          data={"author": "John Doe", "title": "Lorem ipsum dolor sit amet"})
              self.assertEqual(response.status_code, 201)
              self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
              self.assertEqual(response.headers['location'], 'http://localhost:8080/books/1')

              content = response.json()
              self.assertEqual(content['author'], 'John Doe')
              self.assertEqual(content['title'], 'Lorem ipsum dolor sit amet')
              self.assertEqual(content['id'], 1)

Request verifications
---------------------
PyMoq can be used to validate requests.

Example test
^^^^^^^^^^^^
::

  import unittest
  import requests
  from pymoq import pymoq


  class RequestVerificationTestCase(unittest.TestCase):
      def test_request(self):
          mock = pymoq.Mock()
          stub = mock.create_stub('/books', method='post')

          with mock.run():
              requests.post('http://localhost:8080/books',
                            json={'firstName': 'John', 'lastName': 'Doe'}
                            headers={'content-type': 'application/json'})

          stub.assert_requested_once()
          stub.assert_requested_with_header('content-type', 'application/json')
          stub.assert_requested_body_contains('Doe')

