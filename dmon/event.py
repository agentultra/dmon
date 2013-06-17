import math
from collections import namedtuple

import conf
import pubsub


streams = conf.get_streams()


def process_event(event):
    for stream in streams:
        stream.send(event)


pubsub.subscribe(process_event, "events")


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
        return int(math.ceil(self.time + self.ttl))
