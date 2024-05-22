"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record, Phone

def add_address(address_book: AddressBook) -> Command:
    """Returns the 'add-address' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add-address"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two correct arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name and address")
            case 1:
                raise MissingArgumentsError("address")
            case _:
                if not address_book.has_record(command[0]):
                    raise InvalidArgumentsError(f"Contact you are trying to add address to does not exist: {command[0]}")
                return (True, None)

    def action(command: list[str]) -> Event:
        """Add a email to the contact.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact,
            second element is the email.
        """
        record = address_book.find(command[0])
        address = " ".join(command[1:])
        record.add_address(address)
        return Event(EventType.PRINT, {"print": f"Address for {command[0]} added."})

    return lambda: (select, validate, action)
