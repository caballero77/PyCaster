"""This module contains the 'add' command. It adds a new contact to the storage."""
import re
from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record, Phone

def add_email(address_book: AddressBook) -> Command:
    """Returns the 'add-email' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add-email"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two correct arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name and email")
            case 1:
                raise MissingArgumentsError("email")
            case 2:
                if not address_book.has_record(command[0]):
                    raise InvalidArgumentsError(f"Contact you are trying to add email to does not exist: {command[0]}")
                
                email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_pattern, command[1]):
                    raise InvalidArgumentsError(f"Неправильний формат email: {command[1]}")

                # Перевірка, чи email вже існує у інших користувачів
                if not address_book.is_email_unique(command[1]):
                    raise InvalidArgumentsError(f"Email {command[1]} вже використовується у іншого користувача.")

                return (True, None)
            case _:
                raise InvalidArgumentsError("add command takes only one or two arguments.")

    def action(command: list[str]) -> Event:
        """Add a email to the contact.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact,
            second element is the email.
        """
        record = address_book.find(command[0])
        record.add_email(command[1])
        return Event(EventType.PRINT, {"print": f"Email for {command[0]} added."})

    return lambda: (select, validate, action)
