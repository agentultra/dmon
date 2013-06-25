import eventlet

from functools import wraps


__all__ = ["average", "send", "stream", "printer", "when"]


def stream(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return wrapped


def send(event, *targets):
    for target in targets:
        eventlet.spawn_n(target.send, event)


@stream
def when(_test, *targets):
    while True:
        event = (yield)
        if _test(event):
            send(event, *targets)


@stream
def average(round_places, *targets):
    total = 0.0
    count = 0
    while True:
        event = (yield)
        total += float(event.metric)
        count += 1
        avg_event = event._replace(metric=round(total / count, round_places))
        send(avg_event, *targets)


@stream
def printer(prefix):
    while True:
        event = (yield)
        print(prefix, event)
