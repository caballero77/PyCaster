"""This module contains the 'get-note' command. It retrieves a note from the storage by title."""

from typing import Tuple
from datetime import datetime
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook, Note

def get_note(note_book: NoteBook) -> Command:
    """Returns the 'get-note' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-delete'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "get-note"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has one arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("title")
            case 1:
                return (True, None)
            case _:
                raise InvalidArgumentsError("get-note command takes only one argument.")

    def action(command: list[str]) -> Event:
        """Retrieves a note with the given title.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note."""
        note = note_book.find_note_by_title(command[0])
        
        return Event(EventType.PRINT, {"print": str(note)})

    return lambda: (select, validate, action)
