from unittest import TestCase

from dmon.event import Event

class BaseTestCase(TestCase):
    @staticmethod
    def create_event(**kwargs):
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

