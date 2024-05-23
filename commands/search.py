"""Module for the 'search' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, input_error
from storage.address_book import AddressBook

def search(address_book: AddressBook) -> Command:
    """Returns the 'search' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'search'."""
        return len(command) > 0 and (command[0] == "search")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has arguments."""
        if len(command) == 0:
            raise MissingArgumentsError("search command requires at least one argument.")
        return (True, None)

    def action(command: list[str]) -> Event:
        """Search for contacts in the storage."""
        search_str = " ".join(command)
        search_result = address_book.search(search_str)

        if len(search_result) == 0:
            return Event(EventType.PRINT, {"print": "No contacts found."})
        
        info_to_print = "\n".join(
            [str(record) for record in search_result]
        )
        return Event(EventType.PRINT, {"print": info_to_print})

    return lambda: (select, validate, action)
