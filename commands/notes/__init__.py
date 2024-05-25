from .add_note import add_note
from .note_rename import note_rename
from .note_delete import note_delete
from .note_update import note_update
from .get_note import get_note
from .delete_tags import delete_tags
from .add_tags import add_tags
from .note_search import note_search
from .all_notes import all_notes
from storage.note_book import NoteBook

def commands(note_book: NoteBook):
    return [
            add_note(note_book),
            note_rename(note_book),
            note_delete(note_book),
            note_update(note_book),
            delete_tags(note_book),
            add_tags(note_book),
            get_note(note_book),
            note_search(note_book),
            all_notes(note_book)
        ]