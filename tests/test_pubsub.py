import collections
import mock
import unittest

from dmon import pubsub as ps


class TestPubSub(unittest.TestCase):

    def setUp(self):
        ps.topics = collections.defaultdict(list)

    def test_subscribe_adds_callback_for_topic(self):
        def test_callback(a, b, c):
            return [a, b, c]

        ps.subscribe(test_callback, "foo")

        self.assertEqual(ps.topics['foo'][0](), test_callback)

    def test_publish_calls_listeners_for_topic(self):
        def test_callback(value):
            return value

        ps.subscribe(test_callback, "foo")

        with mock.patch("eventlet.GreenPool.spawn_n") as m:
            ps.publish("foo", "bar")
            m.assert_called_once_with(test_callback, "bar")
