class EventEngine:
    def __init__(self):
        # event_name -> list of handlers
        self.listeners = {}

    def register(self, event_type: str, handler):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(handler)

    def emit(self, event_type: str, game, context=None):
        if event_type not in self.listeners:
            return

        for handler in self.listeners[event_type]:
            handler(game, context)