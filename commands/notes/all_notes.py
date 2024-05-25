"""This module contains the 'all-notes' command. It retrieves notes from the storage by tags or keyword."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import InvalidArgumentsError, input_error
from storage.note_book import NoteBook

def all_notes(note_book: NoteBook) -> Command:
    """Returns the 'note-search' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-search'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "all-notes"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has no arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                return (True, None)
            case _:
                raise InvalidArgumentsError("all-notes command takes no arguments.")

    def action(_: list[str]) -> Event:
        """Retrieves all notes."""
        
        if len(note_book.values()) == 0:
            return Event(EventType.PRINT, {"print": "No notes found."})
        
        notes = "\n".join(str(note) for note in note_book.values())
        
        return Event(EventType.PRINT, {"print": str(notes)})

    return lambda: (select, validate, action)
