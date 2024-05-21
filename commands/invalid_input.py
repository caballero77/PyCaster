"""This module contains the 'invalid_input' command."""

from typing import Tuple
from commands.types import CommandValidator, CommandAction
from commands.event import EventType, Event

def action(_: list[str]) -> Event:
    """Return an event with the type 'PRINT' and the message 'Invalid command.'."""
    return Event(EventType.PRINT, {"print": "Invalid command."})

def invalid_input() -> Tuple[CommandValidator, CommandAction]:
    """Returns the 'invalid_input' command.
    Should always be the last command in the list of commands to handle invalid input."""
    return (lambda _: True), (lambda _: (True, None)), action
