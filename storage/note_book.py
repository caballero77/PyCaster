from datetime import datetime
from collections import UserDict

class Note: 
    """Class for note, which contains note title, date and time when a note was created, note body, and tags"""
    def __init__(self, title, datetime, body, tags=None):
        self.title = title
        self.datetime = datetime
        self.body = body
        self.tags = tags if tags is not None else []

    def __str__(self):
        return f'{self.title} {self.datetime} {self.body} Tags: {", ".join(self.tags)}'
    
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
    
    def add_tag(self, tag):
        """Add a tag to the note
        
        Args:
            tag: str: the tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag):
        """Remove a tag from the note
        
        Args:
            tag: str: the tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_note(self, note):
        """Add a new note to the notebook. Title must be unique.
        
        Args:
            note: Note: the note to add
            
        Returns:
            bool: False if a note with the same title already exists, True otherwise
        """
        if note.title in self.data:
            return False
        self.data[note.title] = note
        return True

    def remove_note(self, title):
        """Remove a note from the notebook by its title.
        
        Args:
            title: str: the title of the note to remove
            
        Returns:
            bool: False if a note with the given title is not found, True otherwise
        """
        if title not in self.data:
            return False
        del self.data[title]
        return True

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
        """Search for notes containing the keyword in their title, body, or tags.
        
        Args:
            keyword: str: the keyword to search for
            
        Returns:
            list: a list of string representations of notes containing the keyword
        """
        return [str(note) for note in self.data.values() 
                if keyword.lower() in note.body.lower() 
                or keyword.lower() in note.title.lower()
                or keyword.lower() in [tag.lower() for tag in note.tags]]

    def search_by_tag(self, tag):
        """Search for notes containing a specific tag.
        
        Args:
            tag: str: the tag to search for
            
        Returns:
            list: a list of string representations of notes containing the tag
        """
        return [str(note) for note in self.data.values() if tag.lower() in [t.lower() for t in note.tags]]
