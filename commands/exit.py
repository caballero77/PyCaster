"""This module contains the 'exit' command, which is used to exit the program."""

from typing import Tuple
from commands.types import CommandValidator, CommandAction
from commands.event import EventType, Event
from commands.errors import InvalidArgumentsError, input_error

def select(command: list[str]) -> bool:
    """Check if the command is 'exit' or 'close' and has no arguments.
    
    Args:
        command (list[str]): The command to validate."""
    return len(command) == 1 and (command[0] == "exit" or command[0] == "close")

@input_error
def validate(command: list[str]) -> Tuple[bool, Event]:
    """Check if the command has no arguments."""
    if len(command) >= 1:
        raise InvalidArgumentsError("exit command does not take any arguments.")
    return (True, None)

def action(_: list[str]) -> Event:
    """Return an event with the type 'END' and the message 'Goodbye!'."""
    return Event(EventType.END, {"print": "Goodbye 🙌!", "reason": "User exited the program."})

def exit() -> Tuple[CommandValidator, CommandAction]:
    """Returns the 'exit' command"""
    return select, validate, action
