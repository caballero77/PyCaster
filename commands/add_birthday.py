"""This module contains the 'add-birthday' command. It adds a birthday to a contact."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record, Phone, Birthday

def add_birthday(address_book: AddressBook) -> Command:
    """Returns the 'add-birthday' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add-birthday'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add-birthday"

    @input_error
    def valifate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name and bithday")
            case 1:
                raise MissingArgumentsError("birthday")
            case 2:
                if not address_book.has_record(command[0]):
                    raise InvalidArgumentsError(f"Contact you are trying to update not found: {command[0]}")
                
                if not Birthday.validate(command[1]):
                    raise InvalidArgumentsError(f"Invalid date for birthday: {command[1]}")
                
                return (True, None)
            case _:
                raise InvalidArgumentsError("add-birthday command takes only two arguments.")

    def action(command: list[str]) -> Event:
        """Add a birthday to the contact with the given name.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact,second element is the birthday.
        """
        record = address_book.find(command[0])
        record.add_birthday(command[1])
        return Event(EventType.PRINT, {"print": f"Birthday for {command[0]} added."})
    
    return lambda: (select, valifate, action)
