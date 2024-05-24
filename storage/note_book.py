from datetime import datetime
from collections import UserDict

class Note: 
    """Class for note, which contains note title, date and time when a note was created, and note body"""
    def __init__(self, title, datetime, body):
        self.title = title
        self.datetime = datetime
        self.body = body

    def __str__(self):
        return f'{self.title} {self.datetime} {self.body}'
    
    def change_title(self, title):
        """Change the title of the note
        
        Args:
            title: str: new title of the note
        """
        self.title = title

    def change_body(self, body):
        """Change the body of the note
        
        Args:
            body: str: new body of the note
        """
        self.body = body

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_note(self, note):
        """Add a new note to the notebook. Title must be unique.
        
        Args:
            note: Note: the note to add
            
        Raises:
            ValueError: if a note with the same title already exists
        """
        if note.title in self.data:
            raise ValueError(f'Note with title "{note.title}" already exists.')
        self.data[note.title] = note

    def remove_note(self, title):
        """Remove a note from the notebook by its title.
        
        Args:
            title: str: the title of the note to remove
            
        Raises:
            KeyError: if a note with the given title is not found
        """
        if title not in self.data:
            raise KeyError(f'Note with title "{title}" not found.')
        del self.data[title]

    def find_note_by_title(self, title):
        """Find a note by its title.
        
        Args:
            title: str: the title of the note to find
            
        Returns:
            Note: the note with the given title, or None if not found
        """
        return self.data.get(title)

    def list_notes(self):
        """List all notes in the notebook.
        
        Returns:
            list: a list of string representations of all notes
        """
        return [str(note) for note in self.data.values()]

    def search_by_keyword(self, keyword):
        """Search for notes containing the keyword in their title or body.
        
        Args:
            keyword: str: the keyword to search for
            
        Returns:
            list: a list of string representations of notes containing the keyword
        """
        return [str(note) for note in self.data.values() if keyword.lower() in note.body.lower() or keyword.lower() in note.title.lower()]   
