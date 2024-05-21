from commands.event import EventType
from commands.types import Handler

def command_type_to_lowwer(command: list[str]) -> list[str]:
    """Converts the first element of the command to lowercase to be case insensitive."""
    return [command[0].lower()] + command[1:]

def cli_processor(handler: Handler):
    """Starts the command-line interface processor."""
    def start_processor():
        while True:
            text_command = command_type_to_lowwer(input("Enter command: ").strip().split(" "))
            event = handler(text_command)
            match event.type:
                case EventType.PRINT:
                    print(event.payload["print"])
                    continue
                case EventType.END:
                    print(event.payload["print"])
                    break
                case EventType.ERROR:
                    print(f"Error occurred: {event.payload['message']}")
                    continue
                case _:
                    continue
    return start_processor