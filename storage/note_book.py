from datetime import datetime
from collections import UserDict

class Note: 
    """Class for note, which contains note title, note body, and date and time when a note was created"""
    def __init__(self, title, body, datetime):
        self.title = title
        self.body = body
        self.datetime = datetime

    def __str__(self):
        return f'{self.title} {self.body} {self.datetime}'
    
    def change_title(self, title):
        """Change the title of the note"""
        self.title = title

    def change_body(self, body):
        """Change the body of the note"""
        self.body = body

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()

    def add(self, note):
        """Add a new note to the notebook. Title must be unique."""
        if note.title in self.data:
            print(f'Note with title "{note.title}" already exists.')
        else:
            self.data[note.title] = note

    def remove(self, title):
        """Remove a note from the notebook by its title."""
        if title in self.data:
            del self.data[title]
        else:
            print(f'Note with title "{title}" not found.')

    def find(self, title):
        """Find a note by its title."""
        if title in self.data:
            return self.data[title]
        else:
            print(f'Note with title "{title}" not found.')
            return None

    def list_notes(self):
        """List all notes in the notebook."""
        return [str(note) for note in self.data.values()]

    def search_by_keyword(self, keyword):
        """Search for notes containing the keyword in their title or body."""
        return [str(note) for note in self.data.values() if keyword.lower() in note.body.lower() or keyword.lower() in note.title.lower()]

    def edit_note(self, title, new_title=None, new_body=None):
        """Edit the title and/or body of an existing note."""
        note = self.find(title)
        if note:
            if new_title and new_title != title:
                if new_title in self.data:
                    print(f'Note with title "{new_title}" already exists.')
                    return
                self.data[new_title] = self.data.pop(title)
                note.change_title(new_title)
            if new_body:
                note.change_body(new_body)

