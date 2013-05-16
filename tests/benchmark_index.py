import time
import random

from dmon.index import Index
from dmon.event import Event


def add_random_events(index, total_events, expired_ratio):
    num_expired = int(total_events * expired_ratio)
    num_fresh = total_events - num_expired

    for i in range(num_fresh):
        event = Event(
            host='host-%d' % i,
            service='service',
            state='up',
            description='description',
            time=time.time(),
            ttl=random.randint(300, 600),
            metric=0.5)
        index.update(event)

    for i in range(num_expired):
        age = random.randint(0, 300)
        event = Event(
            host='host-%d' % i,
            service='service',
            state='up',
            description='description',
            time=time.time() - age,
            ttl=age,
            metric=0.5)
        index.update(event)


if __name__ == '__main__':
    while True:
        now = time.time()
        index = Index()
        add_random_events(index, 1000000, 0.10)
        add_event_time = time.time() - now

        now = time.time()
        expired = index.expire(now)
        expired_event_time = time.time() - now

        print 'Add: {:.4f} seconds Expire: {:.4f} seconds'.format(
            add_event_time, expired_event_time)
