from .add_address import add_address
from .add_contact import add_contact
from .add_birthday import add_birthday
from .add_email import add_email
from .birthdays import birthdays
from .change_contact import change_contact
from .delete import delete_field
from .show_all import show_all
from .show_birthday import show_birthday
from .show_phone import show_phone
from .wipe_contact import wipe_contact
from storage.address_book import AddressBook

def commands(address_book: AddressBook) :
    return [
        add_address(address_book),
        add_contact(address_book),
        add_birthday(address_book),
        add_email(address_book),
        birthdays(address_book),
        change_contact(address_book),
        delete_field(address_book),
        show_all(address_book),
        show_birthday(address_book),
        show_phone(address_book),
        wipe_contact(address_book)
    ]