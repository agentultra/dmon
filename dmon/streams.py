import eventlet

from functools import wraps


__all__ = ["coroutine", "printer", "when"]


def coroutine(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return wrapped


@coroutine
def when(_test, target):
    while True:
        event = (yield)
        if _test(event):
            target.send(event)


@coroutine
def printer(prefix):
    while True:
        event = (yield)
        print(prefix, event)
