import json
import unittest

from dmon import event
from dmon import protocol


class TestProtocol(unittest.TestCase):

    def test_get_protocol(self):
        proto = protocol.get_protocol("json")
        self.assertEqual(proto, protocol.JSON)

    def test_get_unsupported_protocol(self):
        self.assertRaises(protocol.UnsupportedProtocolError,
                          protocol.get_protocol,
                          "foo")


class TestJONProtocol(unittest.TestCase):

    def setUp(self):
        self.proto = protocol.JSON()
        self.event = event.Event(host="127.0.0.1",
                                 service="web",
                                 state="online",
                                 description="test",
                                 time=656789,
                                 ttl=3600,
                                 metric=0.5)
        self.event_dict = {'host': "127.0.0.1",
                           'service': "web",
                           'state': "online",
                           'description': "test",
                           'time': 656789,
                           'ttl': 3600,
                           'metric': 0.5}

    def test_implements_read(self):
        self.assertEqual(self.proto.read(json.dumps(self.event_dict)),
                         self.event)

    def test_read_malformed_event(self):
        self.assertRaises(protocol.MalformedEventError,
                          self.proto.read,
                          json.dumps({'foo': "bar"}))

    def test_write(self):
        self.assertEqual(self.proto.write(self.event),
                         json.dumps(self.event_dict))
