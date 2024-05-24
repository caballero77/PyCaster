from .add_note import add_note
from .note_rename import note_rename
from .note_delete import note_delete
from .note_update import note_update
from storage.note_book import NoteBook

def commands(note_book: NoteBook):
    return [
            add_note(note_book),
            note_rename(note_book),
            note_delete(note_book),
            note_update(note_book)
        ]