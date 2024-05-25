"""This module contains the 'note-search' command. It retrieves notes from the storage by tags or keyword."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.note_book import NoteBook, Note

def note_search(note_book: NoteBook) -> Command:
    """Returns the 'note-search' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'note-search'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "note-search"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has at least one argument.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("type and search term")
            case 1:
                raise MissingArgumentsError("search term")
            case 2:
                if command[0] not in ["tag", "keyword"]:
                    raise InvalidArgumentsError("First argument must be 'tag' or 'keyword'.")
                return (True, None)
            case _:
                raise InvalidArgumentsError("note-search command takes at most two arguments.")

    def action(command: list[str]) -> Event:
        """Retrieves notes with the given tags or keyword.
        
        Args:
            command (list[str]): The command to execute. First argument is the type of search, the rest are tag or keyword."""
        
        search_result = []
        if command[0] == "tag":
            search_result = note_book.search_by_tag(command[1])
        else :
            keyword = " ".join(command[1:])
            search_result = note_book.search_by_keyword(keyword)
            
        notes = "\n".join(str(note) for note in search_result)
        
        return Event(EventType.PRINT, {"print": str(notes)})

    return lambda: (select, validate, action)
