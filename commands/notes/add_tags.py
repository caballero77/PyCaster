"""This module contains the 'add-tags' command. It adds a new note to the storage."""

from typing import Tuple
from datetime import datetime
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook, Note

def add_tags(note_book: NoteBook) -> Command:
    """Returns the 'add-note-tags' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add-tags'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add-tags"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has at least two arguments and the note with the given title exists.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("title and tags")
            case 1:
                raise MissingArgumentsError("tags")
            case _:
                if not note_book.find_note_by_title(command[0]):
                    raise InvalidArgumentsError(f"Note with the title {command[0]} does not exist.")
                return (True, None)

    def action(command: list[str]) -> Event:
        """Add tags to the note with the given title.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note, and the rest are tags."""
        title = command[0]
        tags = command[1:] if len(command) > 1 else []

        note = note_book.find_note_by_title(title)
        for tag in tags:
            note.add_tag(tag)
        
        return Event(EventType.PRINT, {"print": f'✅ Tags added to the note "{title}".'})
    return lambda: (select, validate, action)
