from collections import namedtuple


Event = namedtuple('Event', ['host',
                             'service',
                             'state',
                             'description',
                             'time',
                             'ttl',
                             'metric'])
