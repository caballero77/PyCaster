"""Module for the 'search-by-year' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, input_error
from storage.address_book import AddressBook

def search_by_year(address_book: AddressBook) -> Command:
    """Returns the 'search-by-year' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'search-by-year'."""
        return len(command) > 0 and (command[0] == "search-by-year")

    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has arguments."""
        if len(command) == 0:
            raise MissingArgumentsError("search by year command requires one argument.")
        if len(command) > 1:
            raise MissingArgumentsError("search by year command requires only one argument.")
        if not is_integer(command[0]):
            raise MissingArgumentsError("search by year command requires a year as an argument.")
        return (True, None)
        

    def action(command: list[str]) -> Event:
        """Search for contacts in the storage."""
        year = int(command[0])
        search_result = address_book.search_by_birth_year(year)

        if len(search_result) == 0:
            return Event(EventType.PRINT, {"print": "No contacts found."})
        
        info_to_print = "\n".join(
            [str(record) for record in search_result]
        )
        return Event(EventType.PRINT, {"print": info_to_print})

    return lambda: (select, validate, action)
