dmon
====

A stream-processing service for monitoring distributed clusters.

Inspired by Riemann, dmon will use Python coroutines as its
stream-processing language.  An example configuration will look
something like:

    stream = when(lambda event: event['state'] == "warning",
                  email("me@mycompany.com"))

To start a dmon server, you'll first need to write a Python module
with your streams in it.  A stream is just a co-routine that receives
events ("is yielded into"), does some processing, and sends the events
to one or more streams.  Bind your streams at the module level to
names containing the word, "stream".  Then tell dmon about where it
can import your module and it'll handle the rest:

    $ export PYTHONPATH="/path/to/my/module:$PYTHONPATH"
    $ export DMON_STREAM_MODULE="mystream"
    $ cd /to/my/dmon/env && source bin/activate && python dmon/dmon/dmon.py

That should get the UDP listener up and ready to receive events.

For development purposes I've implemented the most rudimentary
protocol possible: JSON.  I plan to eventually add Protocol Buffers
(and maybe Thrift) support in the future.

An event message has the following keys:

- host
- service
- state
- description
- time
- ttl
- metric

And all fields are required.  This will change in the future as I
intend to mirror Riemann's event protocol which allows fields to be
optional.


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
