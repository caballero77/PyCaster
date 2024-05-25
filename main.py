import sys
from pathlib import Path
from processor import cli_processor
from handler import compose_handlers
from commands.handlers import get_handlers
from commands.types import Dependencies
from storage.address_book import AddressBook
from storage.note_book import NoteBook
from contextlib import contextmanager

def build_processor(dependencies: Dependencies):
    handlers = get_handlers(dependencies)
    handler = compose_handlers(handlers)
    return cli_processor(handler)

@contextmanager
def build_dependencies(folder: Path):
    note_book_file = folder / 'note_book.pickle'
    if not note_book_file.exists():
        note_book_file.touch()
    note_book, err = NoteBook.load_data(note_book_file) if note_book_file else (NoteBook(), None)
    if err:
        print(err)
        sys.exit(1)
    
    address_book_file = folder / 'address_book.pickle'
    if not address_book_file.exists():
        address_book_file.touch()
    address_book, err = AddressBook.load_data(address_book_file) if address_book_file else (AddressBook(), None)
    if err:
        print(err)
        sys.exit(1)
    print(f"Data has been loaded from file 💾: {address_book_file} and {note_book_file}")
    try:
        yield Dependencies(address_book, note_book)
    finally:
        note_book.save_data(note_book_file)
        address_book.save_data(address_book_file)
        print(f"Data has been saved to file 📓: {address_book_file} and {note_book_file}")


def main(filename: Path):
    with build_dependencies(filename) as dependencies:
        processor = build_processor(dependencies)
        processor()
        

if __name__ == "__main__":
    default_directory = Path.home() / 'my_address_book'

    if not default_directory.exists():
        default_directory.mkdir(parents=True, exist_ok=True)

    main(default_directory)