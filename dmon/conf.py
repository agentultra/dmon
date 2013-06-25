import importlib
import inspect
import os
import sys


ENVIRONMENT_VARIABLE = 'DMON_STREAM_MODULE'
_streams = None


class ImproperlyConfigured(BaseException): pass


def _import_stream_module():
    try:
        settings_module = os.environ[ENVIRONMENT_VARIABLE]
    except KeyError as e:
        raise ImproperlyConfigured("Missing module name")
    else:
        try:
            mod = importlib.import_module(settings_module)
        except ImportError as e:
            raise ImportError("Could not import stream module '%s' "
                              "(Is it on sys.path?)" % settings_module)
        else:
            return mod


def _get_streams_from_module(mod):
    streams = [getattr(mod, name) for name in dir(mod)
               if inspect.isgenerator(getattr(mod, name))
               and "stream" in name]
    return streams


def get_streams():
    """
    Return a list of stream co-routines.

    Tries to return a cached list of streams.  Otherwise it will try
    importing the user-defined module and extract the list of streams
    from it.
    """
    global _streams

    if _streams:
        return _streams

    mod = _import_stream_module()
    streams = _get_streams_from_module(mod)
    _streams = list(set(streams))
    return _streams
