"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record, Phone

def add_contact(address_book: AddressBook) -> Command:
    """Returns the 'add' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name")
            case 1:
                if address_book.has_record(command[0]):
                    raise InvalidArgumentsError(f"Contact you are trying to add already exists: {command[0]}")
                return (True, None)
            case 2:
                if not Phone.validate(command[1]):
                    raise InvalidArgumentsError(f"Invalid phone number: {command[1]}")
                return (True, None)
            case _:
                raise InvalidArgumentsError("add command takes only one or two arguments.")

    def action(command: list[str]) -> Event:
        """Add a new contact with the given name and phone number.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact,
            second element is the phone number.
        """
        record = address_book.find(command[0])
        if record and len(command) > 1:
            record.add_phone(command[1])
            return Event(EventType.PRINT, {"print": f"Phone number for {command[0]} added."})
        else:
            record = Record(command[0])
            if len(command) > 1:
                record.add_phone(command[1])
            address_book.add_record(record)
            return Event(EventType.PRINT, {"print": f"Contact {command[0]} added."})
    return lambda: (select, validate, action)
