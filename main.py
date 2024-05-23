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
    print(f"Data has been loaded from file: {filename}")
    try:
        yield Dependencies(address_book)
    finally:
        address_book.save_data(filename)
        print(f"Data has been saved to file: {filename}")
            

def main(filename: Path):
    with build_dependencies(filename) as dependencies:
        processor = build_processor(dependencies)
        processor()
        

if __name__ == "__main__":

    #filename = Path(sys.argv[1] if len(sys.argv) > 1 else "address_book.pickle")
    
    # Встановлення шляху до файлу
    file_name = 'address_book.pickle'
    default_directory = Path.cwd() / 'my_address_book'
    #default_directory = Path.home() / 'my_address_book_dir2'
    filename = default_directory / file_name

    # Перевірка, чи файл знаходиться у зазначеній папці
    if not filename.exists():
        # Якщо ні, створюємо директорію
        filename.parent.mkdir(parents=True, exist_ok=True)
        # Оновлюємо шлях до файлу
        filename = filename.parent / file_name

    main(filename)