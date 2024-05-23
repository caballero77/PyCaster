"""Module with the 'wipe' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook

def wipe_contact(address_book: AddressBook) -> Command:
    """Returns the 'wipe' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'wipe'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "wipe"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validates the command.
        
        Args:
            command (list[str]): The command to validate."""
        if len(command) != 2:
            raise MissingArgumentsError("name of the contact.")

        name = command[1]

        if not address_book.has_record(name):
            raise InvalidArgumentsError(f"Contact you are trying to wipe not found: {name}")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Wipe the contact with the given name.

        Args:
            command (list[str]): The command to execute.
            First element is the name of the contact.
        """
        name = command[1]
        address_book.delete(name)

        return Event(EventType.PRINT, {"print": f"Contact {name} wiped from address book."})

    return lambda: (select, validate, action)