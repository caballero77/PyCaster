#  This is module for 'birthdays' 'days' command implementation.
#  This command prints upcoming contacts birthdays for the nearest user-defined upcoming days value.

from datetime import datetime
from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import InvalidArgumentsError, input_error
from storage.address_book import AddressBook, Record


def birthdays(address_book: AddressBook) -> Command:
    """Returns the 'birthdays' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'birthdays'."""
        return len(command) > 0 and (command[0] == "birthdays")  # Check if the input command is 'birthdays' command.

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has no needed argument."""
        if len(command) < 1:  # Check if the input command has no needed argument.
            raise InvalidArgumentsError("'birthdays' command need to take 'days' argument. Input command must be:\n'birthdays 'days' - to show upcoming birthdays in nearest [days].")
        if len(command) >= 2:  # Check if the input command has more arguments than needed.
            raise InvalidArgumentsError("'birthdays' command can take only one argument - 'days' as integer - to show upcoming birthdays in nearest [days].")
        if not command[0].isdigit():  # Check if the input command argument is not a number.
            raise InvalidArgumentsError("'days' argument must be an integer number.")
        return (True, None)  # Return True if the input command is valid, otherwise return False.
                             # Its made for further usage in the code in order to check if the command is valid.
                             # For example, if the command is valid, then the action function will be executed.
                             # Otherwise, the error message will be printed.

    def action(command: list[str]) -> Event:
        """Prints upcoming birthdays for the next week from the address book."""
        days_range = int(command[0])  # Convert the input command number value to integer.
        birthdays_ = address_book.get_upcoming_birthdays(days_range)
        if len(birthdays_) == 0:
            return Event(EventType.PRINT, {"print": f"No upcoming birthdays in nearest {days_range} days found."})
        info_to_print = f"Have found next upcoming birthdays in nearst {days_range} days:\n"\
            + "\n".join(
            [f"{user['name']} - {user['congratulation_date']}" for user in birthdays_]
        )
        return Event(EventType.PRINT, {"print": info_to_print})  # Event is used to return the action result to the processor

    return lambda: (select, validate, action)  
    # Return the 'birthdays' command function. It works as a 'command factory'.
    # 'select' function is used to check if the input command is 'birthdays', otherwise return False.
    # 'validate' function is used to check if the input command is valid, otherwise raise an error.
    # 'action' function is used to execute the command action, like print upcoming birthdays.
    # 'command' function is used in the processor.py module to create a command function with a specific implementation.
