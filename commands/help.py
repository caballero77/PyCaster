"""Module with the 'help' command."""

from commands.types import Command
from commands.event import EventType, Event

def help_command() -> Command:
    """Returns the 'help' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'help'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "help"

    def validate(command: list[str]) -> tuple[bool, Event]:
        """Validates the command.
        
        Args:
            command (list[str]): The command to validate."""
        return (True, None)

    def action(command: list[str]) -> Event:
        """Displays help information.

        Args:
            command (list[str]): The command to execute.
        """
        help_text = """
CLI bot PyCaster v[1.0]
by [team_name]

Supported input commands:

0. To get help:
[help] - show this help text.

1. Adding a new contact:
add [contact_name] - add a new contact only by name.
add [contact_name] [phone] - add a new contact with name and a phone number.

2. Changing or adding contact record details:
change name [contact_name] phone [new_phone] - change (add) contacts phone number.
change name [contact_name] email [new_email] - change (add) contacts email.
change name [contact_name] address [new_address] - change (add) contacts address.
change name [contact_name] birthday [new_birthday] - change (add) contacts birthday.

3. Deleting contact details:
delete name [contact_name] phone - delete all phone numbers of contact.
delete name [contact_name] email - delete the email of contact.
delete name [contact_name] address - delete the address of contact.
delete name [contact_name] birthday - delete the birthday of contact.

4. Deleting an entire contact:
wipe name [contact_name] - delete the entire contact record.

5. Showing phone numbers:
phone [contact_name] - show phone number(s) of a contact.

6. Showing all contacts:
show all - show all contacts.

7. Adding a birthday:
add-birthday [contact_name] [birthday] - add a birthday to a contact in format YYYY-MM-DD.

8. Showing a birthday:
show-birthday [contact_name] - show the birthday of a contact.

9. Showing upcoming birthdays for the next [user_value] days:
birthdays [days_range] - show upcoming birthdays in nearest [days].

10. Add a note:
add-note [note_title] [note_body] - add a new note with a title and body.

11.Rename a note:
rename-note [old_title] [new_title] - rename a note by title.

12. Update a note:
update-note [note_title] [note_body] - update a note by title.

13. Show all notes:
show-notes - show all notes.

14. Delete a note:
delete-note [note_title] - delete a note by title.

15.get note by title:
get-note [note_title] - get note by title.

16. Add note tags:
add-tags [note_title] [tags] - add a tag to a note.

17. Delete note tags:
delete-tags [note_title] [tags] - delete a tag from a note.

18. Search notes by keyword:
note-search keyword [keyword] - search notes by keyword.

19. Search notes by tag:
note-search tag [tag] - search notes by tag.

20. Save data and exit the bot program:
exit or close - exit the program .
"""

        return Event(EventType.PRINT, {"print": help_text})

    return lambda: (select, validate, action)