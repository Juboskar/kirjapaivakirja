class Event:
    def __init__(self, event_type: str, time, content: tuple):
        self.type = event_type
        self.time = time
        self.content = content

def concatenate_event_lists(ratings: tuple, progress_updates: tuple):
    events = []
    for i in ratings:
        events.append(Event("rating", i[5], i))
    for i in progress_updates:
        events.append(Event("progress", i[4], i))
    def order(e: Event):
        return e.time
    events.sort(key=order, reverse=True)
    return events[:30]