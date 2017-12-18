PyMoq
=====
.. image:: https://travis-ci.org/snifter/pymoq.svg?branch=master
    :target: https://travis-ci.org/snifter/pymoq

PyMoq is a tool for mocking HTTP services.


Usage
-----

::

  content = '{"author": "John Doe", "title": "Lorem ipsum dolor sit amet", "id": 1}'
  headers = {
    'content-type': 'application/json; charset=utf-8',
    'location': 'http://localhost:8090/books/1'
  }

  mock = pymoq.Mock(port=8090)
  mock.create_stub('/books', method='post').response(content,
                                                     headers=headers,
                                                     httpStatus=201)

  with mock.run():
      response = requests.post('http://localhost:8090/books',
                        data={"author": "John Doe", "title": "Lorem ipsum dolor sit amet"})
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')
      self.assertEqual(response.headers['location'], 'http://localhost:8090/books/1')
      self.assertEqual(response.text, content)