import eventlet
import unittest

from dmon.event import Event
from dmon.streams import *
from dmon.index import Index
from functools import wraps


class TestStreams(unittest.TestCase):

    def setUp(self):
        self._original_spawn_n = eventlet.spawn_n
        eventlet.spawn_n = self.stub_spawn_n(eventlet.spawn_n)
        self.processed_events = []
        self.index = Index.factory()

    def stub_spawn_n(self, spawn_n):
        @wraps(spawn_n)
        def wrapper(*args, **kwargs):
            func = args[0]
            return func(*args[1:], **kwargs)
        return wrapper

    def tearDown(self):
        eventlet.spawn_n = self._original_spawn_n
        if hasattr(Index, 'instance'):
            del Index.instance
        self.index = None

    def event(self,
              host="123.123.12.1",
              service="web",
              state="available",
              description="Testing",
              time=1370625736,
              ttl=3600,
              metric=0.5):
        return Event(host, service, state,
                     description, time, ttl,
                     metric)

    @stream
    def sink(self):
        while True:
            event = (yield)
            self.processed_events.append(event)

    def test_when(self):
        stream = when(lambda c: c.state == 'offline',
                      self.sink())
        for s in ['online', 'online', 'offline', 'online']:
            stream.send(self.event(state=s))

        self.assertEqual(self.processed_events,
                         [self.event(state='offline')])

    def test_average(self):
        stream = average(2, self.sink())
        for m in [2, 3, 5]:
            stream.send(self.event(metric=m))

        print(self.processed_events)
        self.assertEqual(self.processed_events,
                         [self.event(metric=2.0),
                          self.event(metric=2.5),
                          self.event(metric=3.33)])

    def test_index(self):
        stream = index()
        event = self.event(state='online')
        stream.send(event)
        stored_event = self.index.get(event.host, event.service)
        self.assertEqual(event, stored_event)
