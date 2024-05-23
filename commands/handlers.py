"""This module contains functions for building handlers from commands."""

from commands.types import Command, Handler, Dependencies
from commands.exit import exit
from commands.add_contact import add_contact
from commands.change_contact import change_contact
from commands.show_phone import show_phone
from commands.show_all import show_all
from commands.invalid_input import invalid_input
from commands.hello import hello
from commands.add_birthday import add_birthday
from commands.show_birthday import show_birthday
from commands.birthdays import birthdays
from commands.add_email import add_email
from commands.add_address import add_address
from commands.delete import delete_field
from commands.wipe_contact import wipe_contact
from commands.help import help_command

def build_handler(command: Command) -> Handler:
    """Builds a handler from a command."""
    select, validate, action = command()
    def cmd(command: str, next_command: Command):
        if select(command):
            valid, event = validate(command[1:])
            return action(command[1:]) if valid else event
        
        return next_command
    return cmd

def get_handlers(dependencies: Dependencies):
    """Returns a list of handlers."""
    return list(map(build_handler, [
        exit,
        add_contact(dependencies.address_book),
        change_contact(dependencies.address_book),
        show_phone(dependencies.address_book),
        show_all(dependencies.address_book),
        add_birthday(dependencies.address_book),
        show_birthday(dependencies.address_book),
        birthdays(dependencies.address_book),
        add_email(dependencies.address_book),
        add_address(dependencies.address_book),
        delete_field(dependencies.address_book),
        wipe_contact(dependencies.address_book),
        help_command(),
        hello,
        invalid_input,
    ]))