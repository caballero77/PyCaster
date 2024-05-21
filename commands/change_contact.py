"""Module with the 'change' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Phone

def change_contact(address_book: AddressBook) -> Command:
    """Returns the 'change' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'change'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "change"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Valicates the command.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name, phone number to change and new phone number.")
            case 1:
                raise MissingArgumentsError("phone number to change and new phone number.")
            case 2:
                raise MissingArgumentsError("new phone number.")
            case 3:
                if not address_book.has_record(command[0]):
                    raise InvalidArgumentsError(f"Contact you are trying to update not found: {command[0]}")

                record = address_book.find(command[0])
                if not record.find_phone(command[1]):
                    raise InvalidArgumentsError(f"Phone number you are trying to update not found: {command[1]}")
                
                if not Phone.validate(command[1]):
                    raise InvalidArgumentsError(f"Invalid phone number: {command[1]}")
                
                if not Phone.validate(command[2]):
                    raise InvalidArgumentsError(f"Invalid phone number: {command[2]}")

                return (True, None)
            case _:
                raise InvalidArgumentsError("change command takes only two arguments.")

    def action(command: list[str]) -> Event:
        """Update the contact with the given name and phone number.

        Args:
            command (list[str]): The command to execute.
            First element is the name of the contact, second element is the new phone number.
        """
        record = address_book.find(command[0])
        record.edit_phone(command[1], command[2])

        return Event(EventType.PRINT, { "print": f"Contact {command[0]} changed." })

    return lambda: (select, validate, action)
