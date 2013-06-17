import collections
import eventlet
import weakref


topics = collections.defaultdict(list)
pool = eventlet.GreenPool(200)


def subscribe(func, topic):
    pool.spawn_n(topics[topic].append, weakref.ref(func))


def publish(topic, *args, **kwargs):
    for listener_ref in topics[topic]:
        listener = listener_ref()
        if listener:
            pool.spawn_n(listener, *args, **kwargs)
