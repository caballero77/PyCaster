"""This module contains the Event class and EventType enum. """

from dataclasses import dataclass
from enum import Enum
from typing import Dict

class EventType(Enum):
    """The type of event that can be returned by a command."""
    END = 0 # The program should end
    CONTINUE = 1 # The program should continue
    PRINT = 2 # The program should print a message and continue
    ERROR = 3 # The program should print an error message and continue

@dataclass
class Event():
    """The event returned by a command."""
    type: EventType
    payload: Dict[str, str]
