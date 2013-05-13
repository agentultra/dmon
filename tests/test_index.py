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

    @raises(NotImplementedError)
    def test_delete(self):
        event = self.create_event()
        self.index.delete(event)

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
        self.index.update(event)
        self.assertTrue((event.host, event.service) in self.index_dict)

    @raises(NotImplementedError)
    def test_get(self):
        self.index.get('host.name', 'service name')

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
