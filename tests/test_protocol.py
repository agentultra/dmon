import unittest

from dmon import protocol


class TestProtocol(unittest.TestCase):

    def test_get_protocol(self):
        proto = protocol.get_protocol("json")
        self.assertEqual(proto, protocol.JSON)

    def test_get_unsupported_protocol(self):
        self.assertRaises(protocol.UnsupportedProtocolError,
                          protocol.get_protocol,
                          "foo")
