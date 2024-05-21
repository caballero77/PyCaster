import sys
from pathlib import Path
from processor import cli_processor
from handler import compose_handlers
from commands.handlers import get_handlers
from commands.types import Dependencies
from storage.address_book import AddressBook
from contextlib import contextmanager

def build_processor(dependencies: Dependencies):
    handlers = get_handlers(dependencies)
    handler = compose_handlers(handlers)
    return cli_processor(handler)

@contextmanager
def build_dependencies(filename: Path):
    address_book, err = AddressBook.load_data(filename) if filename else (AddressBook(), None)
    if err:
        print(err)
        sys.exit(1)
    print(f"Data has been loaded from file: {filename.name}")
    try:
        yield Dependencies(address_book)
    finally:
        address_book.save_data(filename)
        print(f"Data has been saved to file: {filename.name}")
            

def main(filename: Path):
    with build_dependencies(filename) as dependencies:
        processor = build_processor(dependencies)
        processor()
        

if __name__ == "__main__":
    filename = Path(sys.argv[1] if len(sys.argv) > 1 else "address_book.pickle")
    main(filename)