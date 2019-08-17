from collections import deque, defaultdict
from weakref import ref

class EventHandler:
    def recv_event(self, evt):
        pass

class EventManager:
    def __init__(self):
        self.num_handlers = defaultdict(list)
        self.posting_evts = deque()

    def bind(self, num, handler):
        self.num_handlers[num].append(ref(handler))

    def send(self, evt):
        handlers = self.num_handlers.get(evt.num)
        if handlers:
            for handler_ref in handlers:
                handler = handler_ref()
                if handler:
                    handler.recv_event(evt)

    def post(self, evt):
        self.posting_evts.append(evt)

    def pump(self):
        while self.posting_evts:
            evt = self.posting_evts.popleft()
            self.send_event(evt)
