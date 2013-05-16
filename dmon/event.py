from collections import namedtuple


EVENT_ATTRS = [
    'host',
    'service',
    'state',
    'description',
    'time',
    'ttl',
    'metric'
]

class Event(namedtuple('Event', EVENT_ATTRS)):
    __slots__ = ()

    @property
    def index_key(self):
        return (self.host, self.service)

    @property
    def deadline(self):
        return int(self.time + self.ttl)
