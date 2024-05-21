"""This module contains the 'show_phone' command.
It returns the 'phone' command, which prints the phone number of the contact with the given name."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import input_error, MissingArgumentsError, InvalidArgumentsError
from storage.address_book import AddressBook

def show_phone(address_book: AddressBook) -> Command:
    """Returns the 'phone' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'phone'."""
        return len(command) > 0 and (command[0] == "phone")

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validate the command.
        
        Args:
            command (list[str]): The command to validate."""
        if len(command) == 0:
            raise MissingArgumentsError("name")

        if not address_book.has_record(command[0]):
            raise InvalidArgumentsError(f"Contact you are trying to get not found: {command[0]}")

        if len(command) > 1:
            raise InvalidArgumentsError("phone command takes only one argument.")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Print the phone number of the contact with the given name.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact.
            
        Returns:
            Event: The event with the type 'PRINT' and the phone number of the contact."""
        record = address_book.find(command[0])
        return Event(EventType.PRINT, {"print": "\n".join(map(str, record.phones))})

    return lambda: (select, validate, action)