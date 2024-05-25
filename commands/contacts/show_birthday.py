"""This module contains the 'show_birthday' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import input_error, MissingArgumentsError, InvalidArgumentsError
from storage.address_book import AddressBook

def show_birthday(address_book: AddressBook) -> Command:
    """Returns the 'show-birthday' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'phone'."""
        return len(command) > 0 and (command[0] == "show-birthday")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validate the command.
        
        Args:
            command (list[str]): The command to validate."""
        if len(command) == 0:
            raise MissingArgumentsError("name")

        if not address_book.has_record(command[0]):
            raise InvalidArgumentsError(f"Contact you are trying to get not found: {command[0]}")
        
        if not address_book.find(command[0]).birthday:
            raise InvalidArgumentsError(f"Contact {command[0]} has no birthday.")

        if len(command) > 1:
            raise InvalidArgumentsError("show_birthday command takes only one argument.")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Print the birthday of the contact with the given name.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact.
            
        Returns:
            Event: The event with the type 'PRINT' and the birthday of the contact."""
        record = address_book.find(command[0])
        return Event(EventType.PRINT, {"print": "🎂 " + str(record.birthday)})

    return lambda: (select, validate, action)