"""This module contains the types for the commands."""

from typing import Callable, Tuple, NamedTuple
from commands.event import Event
from storage.address_book import AddressBook
from storage.note_book import NoteBook

CommandSelector = Callable[[list[str]], bool]
"""A function that selects a command."""

CommandValidator = Callable[[list[str]], bool]
"""A function that validates a command."""

CommandAction = Callable[[list[str]], Event]
"""A function that executes a command and returns an event."""

Command = Callable[[], Tuple[CommandSelector, CommandValidator, CommandAction]]
"""A function that returns a command validator and a command action."""

Handler = Callable[[list[str], Command], Command | Event]
"""A function that handles a command and returns a command or an event."""

class Dependencies(NamedTuple):
    """A named tuple that contains the external dependencies for the commands."""
    address_book: AddressBook
    """The storage to use for the contacts related commands."""
    note_book: NoteBook
    """The storage to use for the notes related commands."""
