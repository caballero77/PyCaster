"""This module contains the 'add-note' command. It adds a new note to the storage."""

from typing import Tuple
from datetime import datetime
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook, Note

def add_note(note_book: NoteBook) -> Command:
    """Returns the 'add-note' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add-note'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add-note"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has at least two arguments and the note with the given title does not exist.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("title and body")
            case 1:
                raise MissingArgumentsError("body")
            case _:
                if note_book.find_note_by_title(command[0]):
                    raise InvalidArgumentsError(f"Note with the title {command[0]} already exists.")
                return (True, None)

    def action(command: list[str]) -> Event:
        """Add a new note with the given title and body.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note, second is the body"""
        title = command[0]
        creation_time = datetime.now()
        body = " ".join(command[1:])

        note = Note(title, creation_time, body)
        note_book.add_note(note)
        
        return Event(EventType.PRINT, {"print": f'✅ Note "{title}" added.'})
    return lambda: (select, validate, action)
