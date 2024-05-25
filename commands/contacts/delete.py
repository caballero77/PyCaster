"""Module with the 'delete' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook

def delete_field(address_book: AddressBook) -> Command:
    """Returns the 'delete' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'delete'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "delete"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validates the command.
        
        Args:
            command (list[str]): The command to validate."""
        if len(command) != 2:
            raise MissingArgumentsError("needs arguments of [name] and [field type] that must be deleted.")

        name, field_type = command[0], command[1]

        if not address_book.has_record(name):
            raise InvalidArgumentsError(f"Contact you are trying to update not found: {name}")

        if field_type not in ["phone", "email", "birthday", "address"]:
            raise InvalidArgumentsError(f"Unknown field type: {field_type}")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Delete the field from the contact with the given name.

        Args:
            command (list[str]): The command to execute.
            First element is the name of the contact, second element is the field type.
        """
        name, field_type = command[0], command[1]
        record = address_book.find(name)

        match field_type:
            case "phone":
                record.phones.clear()  # Delete all phones
            case "email":
                record.delete_email()
            case "address":
                record.delete_address()
            case "birthday":
                record.delete_birthday()

        return Event(EventType.PRINT, {"print": f"{field_type.capitalize()} for contact {name} deleted."})

    return lambda: (select, validate, action)