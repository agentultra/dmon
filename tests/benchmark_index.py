import time
import random

from dmon.index import Index
from dmon.event import Event

CURRENT_TIME = time.time()

def add_random_events(index, total_events, expired_ratio):
    num_expired = int(total_events * expired_ratio)
    num_fresh = total_events - num_expired

    for i in range(num_fresh):
        event = Event(
            host='host-%d' % i,
            service='service',
            state='up',
            description='description',
            time=CURRENT_TIME,
            ttl=random.randint(300, 600),
            metric=0.5)
        index.update(event)

    for i in range(num_expired):
        event = Event(
            host='host-%d' % i,
            service='service',
            state='up',
            description='description',
            time=CURRENT_TIME - random.randint(1, 300),
            ttl=0,
            metric=0.5)
        index.update(event)


if __name__ == '__main__':
    while True:
        now = time.time()
        index = Index()
        add_random_events(index, 1000000, 0.10)
        add_event_time = time.time() - now

        now = time.time()
        expired = index.expire(CURRENT_TIME)
        expired_event_time = time.time() - now
        num_expired = len(expired)

        print ('Add: {:.4f} seconds '
               'Expire: {:.4f} seconds '
               'Expired: {} events'.format(
                   add_event_time, expired_event_time, num_expired))
