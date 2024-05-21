from commands.event import EventType, Event
from functools import reduce
from commands.types import Handler

def compose_handlers(handlers: list[Handler]):
    """Compose a list of handlers into a single handler.
    
    Args:
        handlers (list[Handler]): The list of handlers to compose.
    
    Returns:
        Handler: The composed handler."""
    def handler(command: list[str]) -> Event:
        def reducer(result: Handler | Event, next: Handler):
            if isinstance(result, Event):
                return result
            return result(command, next)
        
        handlers.append(Event(EventType.CONTINUE, {}))

        return reduce(reducer, handlers, lambda _, next: next)

    return handler

