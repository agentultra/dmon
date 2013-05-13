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

    def test_clear(self):
        self.index_dict['not'] = 'empty'
        self.index.clear()
        self.assertEquals(self.index_dict, {})

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

    def test_update(self):
        event = self.create_event()
        updated_event = self.index.update(event)
        self.assertTrue((event.host, event.service) in self.index_dict)
        self.assertEquals(event, updated_event)

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
    NUM_HOSTS = 100
    NUM_SERVICES_PER_HOST = 100
    CURRENT_TIME = 1000000
    TTL = 60

    def setUp(self):
        self.index = Index()
        self.add_events()

    def add_events(self):
        host_names = map(lambda(i): 'host-%s' % i, range(self.NUM_HOSTS))
        service_names = map(lambda(i): 'service-%s' % i,
                            range(self.NUM_SERVICES_PER_HOST))
        for host_name in host_names:
            for service_name in service_names:
                event = self.create_event(
                    host=host_name,
                    service=service_name,
                    time=self.CURRENT_TIME,
                    ttl=self.TTL)
                self.index.update(event)

    def test_expire_none_returns_none(self):
        current_expiry_time = self.CURRENT_TIME
        expired_events = self.index.expire(expiry_time=current_expiry_time)
        self.assertEquals(len(expired_events), 0)

    def test_expire_none_removes_none(self):
        num_events = len(self.index)
        current_expiry_time = self.CURRENT_TIME
        expired_events = self.index.expire(expiry_time=current_expiry_time)
        self.assertEquals(len(self.index), num_events)

    def test_expire_all_removes_all(self):
        future_expiry_time = self.CURRENT_TIME + self.TTL + 1
        expired_events = self.index.expire(expiry_time=future_expiry_time)
        self.assertEquals(len(self.index), 0)

    def test_expire_all_returns_all(self):
        num_events = len(self.index)
        future_expiry_time = self.CURRENT_TIME + self.TTL + 1
        expired_events = self.index.expire(expiry_time=future_expiry_time)
        self.assertEquals(len(expired_events), num_events)
