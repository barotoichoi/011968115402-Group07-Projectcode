from enum import Enum

class State(Enum):
    RUNNING = "Running"
    WAITING = "Waiting"
    BLOCKED = "Blocked"
