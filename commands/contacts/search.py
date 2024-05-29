"""This module contains the 'show_birthday' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import input_error, MissingArgumentsError, InvalidArgumentsError
from storage.address_book import AddressBook

def search(address_book: AddressBook) -> Command:
    """Returns the 'show-birthday' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'phone'."""
        return len(command) > 0 and (command[0] == "search")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validate the command.
        
        Args:
            command (list[str]): The command to validate."""
        if len(command) == 0:
            raise MissingArgumentsError("name")

        if len(command) > 1:
            raise InvalidArgumentsError("show_birthday command takes only one argument.")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Print the birthday of the contact with the given name.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact.
            
        Returns:
            Event: The event with the type 'PRINT' and the birthday of the contact."""
        info_to_print = "\n".join(
            [str(record) for record in address_book.values() if (command[0] in str(record.name))]
        )
        if not info_to_print:
            info_to_print = f"🔍 No contacts found."
        return Event(EventType.PRINT, {"print": info_to_print})

    return lambda: (select, validate, action)