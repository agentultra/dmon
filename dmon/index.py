from collections import defaultdict


class Index(object):
    def __init__(self, store=None):
        if store is None:
            store = dict()
        self.store = store
        self.deadlines = defaultdict(list)

    def clear(self):
        """Resets the index"""
        self.store.clear()
        self.deadlines.clear()

    def delete(self, event):
        """Deletes any event in the index with a matching host and service.

        Returns the deleted event, if found; None, otherwise.
        """
        deleted_event = self.store.pop(self._event_key(event), None)
        if deleted_event is not None:
            deadline = int(deleted_event.time + deleted_event.ttl)
            self.deadlines[deadline].remove(self._event_key(deleted_event))
        return deleted_event

    def expire(self, expiry_time=None):
        """Removes all expired events from the index.

        Returns a list of events removed from the index.
        """
        expire_events = list()
        for event in self.store.viewvalues():
            age = expiry_time - event.time
            if age >= event.ttl:
                expire_events.append(event)
        for event in expire_events:
            self.delete(event)

        return expire_events

    def search(self, query):
        """Returns a list of events matching a query AST."""
        raise NotImplementedError()

    def update(self, event):
        """Adds an event to the index"""
        if event.state != 'expired':
            self.store[self._event_key(event)] = event
            deadline = int(event.time + event.ttl)
            self.deadlines[deadline].append(self._event_key(event))
            return event
        else:
            return None

    def get(self, host, service):
        """Finds an event in the index."""
        event_key = (host, service)
        return self.store.get(event_key)

    def __len__(self):
        return len(self.store)

    def __nonzero__(self):
        return True

    def _event_key(self, event):
        return (event.host, event.service)
