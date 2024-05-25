"""Module with the 'change' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Phone, Email, Address, Birthday

def change_contact(address_book: AddressBook) -> Command:
    """Returns the 'change' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'change'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "change"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Validates the command.
        
        Args:
            command (list[str]): The command to validate."""
        if not 3 <= len(command) < 5:  # modified to fit both cases: to edit values and changing phone number
            raise MissingArgumentsError("must be [name], [field type], and [value]\n" + \
                                        "or [old phone] and [new phone] values in case of changing existing phone number")

        name, field_type, new_value = command[0], command[1], command[-1]

        if not address_book.has_record(name):
            raise InvalidArgumentsError(f"Contact you are trying to update not found: {name}")

        if field_type == "phone":
            if not Phone.validate(new_value):
                raise InvalidArgumentsError(f"Invalid phone number: {new_value}. Examples of correct one: +380123456789 or 0123456789.")
            if not address_book.is_phone_unique(new_value):
                raise InvalidArgumentsError(f"Phone number {new_value} already exists in the address book.")
        elif field_type == "email":
            if not Email.validate(new_value):
                raise InvalidArgumentsError(f"Invalid email: {new_value}")
            if not address_book.is_email_unique(new_value): 
                raise InvalidArgumentsError(f"Email {new_value} already exists in the address book.") 
        elif field_type == "birthday":
            if not Birthday.validate(new_value):
                raise InvalidArgumentsError(f"Invalid birthday format: {new_value}")
            # if {new_value} == not address_book.is_email_unique(new_value): 
            #     raise InvalidArgumentsError(f"Email {new_value} already exists in the address book.") 
        elif field_type == "address":
            pass  # No validation for address
        else:
            raise InvalidArgumentsError(f"Unknown field type: {field_type}")

        return (True, None)

    def action(command: list[str]) -> Event:
        """Update the contact with the given name and field.

        Args:
            command (list[str]): The command to execute.
            First element is the name of the contact, second element is the field type, third element is the new value.
        """
        name, field_type, new_value = command[0], command[1], command[-1]
        record = address_book.find(name)

        match field_type:
            case "phone":
                if len(command) == 3:  # will add new phone if 1 argument (new phone) in the 'change [name] phone' command
                    record.add_phone(new_value)
                elif len(command) == 4:  # will change to new phone if 2 arguments (old phone, new phone) in the command
                    old_value = command[-2] 
                    record.edit_phone(old_value, new_value) 
            case "email":
                record.edit_email(new_value)
            case "address":
                record.edit_address(new_value)
            case "birthday":
                record.edit_birthday(new_value)

        return Event(EventType.PRINT, {"print": f"✅ Contact {name} changed."})

    return lambda: (select, validate, action)