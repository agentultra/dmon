dmon
====

A stream-processing service for monitoring distributed clusters.

Inspired by Riemann, dmon will use Python coroutines as its
stream-processing language.  An example configuration will look
something like:

    stream = when(lambda event: event['state'] == "warning",
                  email("me@mycompany.com"))

I'm currently experimenting with using eventlet as the underlying IO
loop.  The goal for this project is to experiment with integrating
into OpenStack for light-weight cluster monitoring.

For development purposes I've implemented the most rudimentary
protocol possible: JSON.  I plan to eventually add Protocol Buffers
(and maybe Thrift) support in the future.


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
