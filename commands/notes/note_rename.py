"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from datetime import datetime
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook

def note_rename(note_book: NoteBook) -> Command:
    """Returns the 'note-delete' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-rename'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "note-rename"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("old and new title")
            case 1:
                raise MissingArgumentsError("new title")
            case 2:
                if not note_book.find_note_by_title(command[0]):
                    raise InvalidArgumentsError(f"Note with the title {command[0]} not found.")
                if note_book.find_note_by_title(command[1]):
                    raise InvalidArgumentsError(f"Note with the title {command[1]} already exists.")
                return (True, None)
            case _:
                raise InvalidArgumentsError("note-rename command takes only one argument.")

    def action(command: list[str]) -> Event:
        """Renames a note with the given title and new title.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note,
            second element is the new title of the note."""
        note_book.rename_note(command[0], command[1])

        return Event(EventType.PRINT, {"print": f'✅ Note "{command[0]}" renamed.'})

    return lambda: (select, validate, action)
