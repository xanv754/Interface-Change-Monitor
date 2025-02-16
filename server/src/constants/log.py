"""All types of messages that can be stored in the system's .log file."""

from enum import Enum


class LogType(Enum):
    """Type of message that can be stored in the system's .log file.

    - ERROR: Error message.
    - WARNING: Warning message.
    - INFO: Information message.
    """

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
