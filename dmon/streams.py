from functools import wraps


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
def printer():
    while True:
        event = (yield)
        print(event)
