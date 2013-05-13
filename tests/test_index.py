from unittest import TestCase
from nose.tools import raises

from dmon.index import Index
from dmon.event import Event


class IndexTestCase(TestCase):
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

    @raises(NotImplementedError)
    def test_expire(self):
        event = self.create_event()
        self.index.expire()

    @raises(NotImplementedError)
    def test_search(self):
        query_ast = []
        self.index.search(query_ast)

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

    def create_event(self, **kwargs):
        default_event_attrs = {
            'host': 'host.name',
            'service': 'service name',
            'state': 'up',
            'description': 'text description',
            'time': 1368210977,
            'ttl': 600,
            'metric': 'tps'
        }
        event_attrs = {attr: kwargs.get(attr, default_event_attrs[attr])
                       for attr in default_event_attrs.iterkeys()}
        event = Event(**event_attrs)
        return event
