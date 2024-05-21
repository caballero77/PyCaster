"""Custom exceptions for the commands module."""

from commands.event import Event, EventType

class MissingArgumentsError(Exception):
    """Exception raised when the command is missing arguments."""
    def __init__(self, message):
        self.message = f"Missing arguments: {message}"
        super().__init__(self.message)


class InvalidArgumentsError(Exception):
    """Exception raised when the command has invalid arguments."""
    def __init__(self, message):
        self.message = f"Invalid arguments: {message}"
        super().__init__(self.message)

def input_error(func):
    """Decorator to catch input errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MissingArgumentsError as e:
            return (False, Event(EventType.ERROR, {"message": e.message}))
        except InvalidArgumentsError as e:
            return (False, Event(EventType.ERROR, {"message": e.message}))
        except Exception as e:
            return (False, Event(EventType.ERROR, {"message": f"Unknown error: {e}"}))
    return wrapper
