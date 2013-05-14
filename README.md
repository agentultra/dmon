dmon
====

A stream-processing service for monitoring distributed clusters.

Inspired by Riemann, dmon will use Python coroutines as its
stream-processing language.  An example configuration will look
something like:

    stream = when(lambda event: event['state'] == "warning",
                  email("me@mycompany.com"))

I'm currently experimenting with using Tornado as the underlying IO
loop.  It doesn't have great support for UDP but that is only one
small part of this application that it doesn't really matter right
now.

For development purposes I've implemented the most rudimentary
protocol possible: JSON.  I plan to eventually add Protocol Buffers
(and maybe Thrift) support in the future.

I'm developing on Python 3.3 because it's awesome.


Testing
-------

To run the unit tests:

    $ python setup.py test

# TODO #

- protocol
  - protobuf
  - thrift ?
  - jsonschema ?
- stream processing
- event storage / querying
- web socket support
- packaging
