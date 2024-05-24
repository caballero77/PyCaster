"""Module for the 'all' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import InvalidArgumentsError, input_error
from storage.address_book import AddressBook

def show_all(address_book: AddressBook) -> Command:
    """Returns the 'all' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'all'."""
        return len(command) > 0 and (command[0] == "all")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has no arguments."""
        if len(command) >= 1:
            raise InvalidArgumentsError("all command does not take any arguments.")
        return (True, None)

    def action(_: list[str]) -> Event:
        """Print all contacts in the storage."""
        info_to_print = "\n".join(
            [str(record) for record in address_book.values()]
        ) if len(address_book.values()) > 0 else "No contacts found."
        return Event(EventType.PRINT, {"print": info_to_print})

    return lambda: (select, validate, action)
