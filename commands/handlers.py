"""This module contains functions for building handlers from commands."""

from commands.types import Command, Handler, Dependencies
from commands.exit import exit
from commands.invalid_input import invalid_input
from commands.hello import hello
from commands.contacts.wipe_contact import wipe_contact
from commands.help import help_command
from commands.contacts import commands as contacts_commands
from commands.notes import commands as note_commands

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
    utility_commands = [
        exit,
        help_command(),
        hello,
        invalid_input,
    ]
    return list(map(build_handler, note_commands(dependencies.note_book) + contacts_commands(dependencies.address_book) + utility_commands))