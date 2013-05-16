from unittest import TestCase
from nose.tools import raises

from dmon.index import Index

from .base import BaseTestCase


class IndexTestCase(BaseTestCase):
    def setUp(self):
        self.index_dict = {}
        self.index = Index(self.index_dict)

    def test_default_constructor(self):
        self.index = Index()
        self.assertEquals(self.index.store, dict())

    def test_clear_empties_index(self):
        event = self.create_event()
        self.index.update(event)
        self.index.clear()
        self.assertEquals(self.index_dict, {})

    def test_clear_empties_deadlines(self):
        event = self.create_event()
        self.index.update(event)
        self.index.clear()
        self.assertEquals(self.index.deadlines, {})

    def test_delete(self):
        event = self.create_event()
        self.index.update(event)
        deleted_event = self.index.delete(event)
        self.assertEquals(self.index_dict, {})
        self.assertEquals(event, deleted_event)

    def test_delete_event_does_not_exist(self):
        event = self.create_event()
        deleted_event = self.index.delete(event)
        self.assertEquals(self.index_dict, {})
        self.assertEquals(deleted_event, None)

    def test_delete_removes_deadline(self):
        event = self.create_event()
        self.index.update(event)
        deleted_event = self.index.delete(event)
        self.assertTrue(all(len(deadlines) == 0
                            for deadlines in self.index.deadlines.values()))

    def test_update(self):
        event = self.create_event()
        updated_event = self.index.update(event)
        self.assertTrue((event.host, event.service) in self.index_dict)
        self.assertEquals(event, updated_event)

    def test_update_deadline(self):
        event = self.create_event(time=0.0, ttl=0)
        updated_event = self.index.update(event)
        self.assertTrue(
            (event.host, event.service) in self.index.deadlines[event.deadline])

    def test_update_expired_event(self):
        event = self.create_event(state='expired')
        updated_event = self.index.update(event)
        self.assertFalse((event.host, event.service) in self.index_dict)
        self.assertEquals(updated_event, None)

    def test_get_event_exists(self):
        event = self.create_event()
        self.index.update(event)

        event_key = (event.host, event.service)
        found_event = self.index.get(*event_key)
        self.assertEquals(event, found_event)

    def test_get_event_does_not_exist(self):
        event = self.create_event()
        event_key = (event.host, event.service)
        found_event = self.index.get(*event_key)
        self.assertEquals(found_event, None)

    def test_len(self):
        event = self.create_event()
        self.index.update(event)
        self.assertEquals(len(self.index), 1)

    def test_bool_empty(self):
        self.assertTrue(self.index)

    def test_bool_non_empty(self):
        event = self.create_event()
        self.index.update(event)
        self.assertTrue(self.index)

    @raises(NotImplementedError)
    def test_search(self):
        query_ast = []
        self.index.search(query_ast)


class IndexExpireTestCase(BaseTestCase):
    CURRENT_TIME = 1000000000.0

    def setUp(self):
        self.index = Index()

    def assertExpiredEvents(self, time, expected):
        expired = self.index.expire(time)
        expired.sort()
        expected.sort()
        self.assertEquals(expired, expected)

    def test_no_events_in_index(self):
        self.assertExpiredEvents(self.CURRENT_TIME, [])

    def test_exipre_single_event(self):
        event = self.create_event(time=self.CURRENT_TIME, ttl=0)
        self.index.update(event)
        self.assertExpiredEvents(self.CURRENT_TIME, [event])

    def test_no_expired_events(self):
        event = self.create_event(time=self.CURRENT_TIME, ttl=1)
        self.index.update(event)
        self.assertExpiredEvents(self.CURRENT_TIME, [])

    def test_no_expired_events_subsecond(self):
        event = self.create_event(time=self.CURRENT_TIME + 0.05, ttl=0)
        self.index.update(event)
        self.assertExpiredEvents(self.CURRENT_TIME, [])

    def test_expire_multiple_events(self):
        expired_events = [
            self.create_event(
                host='test-%d' % i,
                service='expired',
                time=self.CURRENT_TIME,
                ttl=0)
            for i in range(100)
        ]
        fresh_events = [
            self.create_event(
                host='test-%d' % i,
                service='fresh',
                time=self.CURRENT_TIME,
                ttl=1)
            for i in range(100)
        ]
        for event in expired_events + fresh_events:
            self.index.update(event)
        self.assertExpiredEvents(self.CURRENT_TIME, expired_events)

    def test_expire_older_events(self):
        current_event = self.create_event(
            host='test-1',
            service='expired',
            time=self.CURRENT_TIME,
            ttl=0)
        self.index.update(current_event)
        older_event = self.create_event(
            host='test-2',
            service='expired',
            time=self.CURRENT_TIME - 1,
            ttl=0)
        self.index.update(older_event)
        self.assertExpiredEvents(
            self.CURRENT_TIME, [current_event, older_event])
