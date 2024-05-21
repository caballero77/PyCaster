"""Module for the 'birthdays' command. Returns upcoming birthdays for the next week from address book"""

from datetime import datetime
from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record

def birthdays(address_book: AddressBook) -> Command:
    """Returns the 'birthdays' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'birthdays'."""
        return len(command) > 0 and (command[0] == "birthdays")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has no arguments."""
        if len(command) >= 1:
            raise InvalidArgumentsError("birthdays command does not take any arguments.")
        return (True, None)

    def action(_: list[str]) -> Event:
        """Prints upcoming birthdays for the next week from the address book."""
        birthdays = address_book.get_upcoming_birthdays()
        if len(birthdays) == 0:
            return Event(EventType.PRINT, {"print": "No upcoming birthdays found."})
        info_to_print = "\n".join(
            [f"{user['name']} - {user['congratulation_date']}" for user in birthdays ]
        )
        return Event(EventType.PRINT, {"print": info_to_print})

    return lambda: (select, validate, action)
