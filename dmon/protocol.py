import abc
import json

from event import Event


class EventProtocol(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self, _bytes):
        """
        Return an Event object.

        Parse the passed in bytes and return an Event object.
        """

    @abc.abstractmethod
    def write(self, event):
        """
        Return a serialized byte string appropriate for the wire.
        """


class JSON(EventProtocol):
    """
    A basic JSON protocol implementation.

    This class is meant to be used for debugging and development.
    """

    def read(self, _bytes):
        raw_obj = json.loads(str(_bytes, 'utf-8'))
        return Event(**raw_obj)

    def write(self, event):
        ev = {k: getattr(k, event) for k in event._fields}
        return bytes(json.dumps(ev).encode('utf-8'))
