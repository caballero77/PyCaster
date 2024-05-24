"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook

def note_update(note_book: NoteBook) -> Command:
    """Returns the 'note-update' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-update'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "note-update"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("title and new body")
            case 1:
                raise MissingArgumentsError("new body")
            case 2:
                if not note_book.find_note_by_title(command[0]):
                    raise InvalidArgumentsError(f"Note with the title {command[0]} not found.")
                return (True, None)
            case _:
                raise InvalidArgumentsError("note-rename command takes only one argument.")

    def action(command: list[str]) -> Event:
        """Updates a note with the given title and new body.
        
        Args:
            command (list[str]): The command to execute. First element is the title of the note,
            second element is the new body of the note."""
        note_book.update_note_body(command[0], command[1])

        return Event(EventType.PRINT, {"print": f'Note "{command[0]}" updated.'})

    return lambda: (select, validate, action)
