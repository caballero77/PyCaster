"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from datetime import datetime
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook, Note

def note_delete(note_book: NoteBook) -> Command:
    """Returns the 'note-delete' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-delete'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "note-delete"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("title")
            case 1:
                return (True, None)
            case _:
                raise InvalidArgumentsError("note-delete command takes only one argument.")

    def action(command: list[str]) -> Event:
        """Deletes a note with the given title.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note."""
        note_book.remove_note(command[0])

        return Event(EventType.PRINT, {"print": f'Note "{command[0]}" deleted.'})

    return lambda: (select, validate, action)
