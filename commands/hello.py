"""This module contains the 'hello' command."""

from typing import Tuple
from commands.types import CommandValidator, CommandAction
from commands.event import EventType, Event
from commands.errors import InvalidArgumentsError, input_error

def select(command: list[str]) -> bool:
    """Check if the command is 'hello'.
    
    Args:
        command (list[str]): The command to validate."""
    return len(command) == 1 and (command[0] == "hello")

@input_error
def validate(command: list[str]) -> Tuple[bool, Event]:
    """Check if the command has no arguments."""
    if len(command) >= 1:
        raise InvalidArgumentsError("hello command does not take any arguments.")
    return (True, None)

def action(_: list[str]) -> Event:
    """Return an event with the type 'PRINT' and the message 'How can I help you?'."""
    return Event(EventType.PRINT, {"print": "How can I help you?"})

def hello() -> Tuple[CommandValidator, CommandAction]:
    """Returns the 'hello' command"""
    return select, validate, action
