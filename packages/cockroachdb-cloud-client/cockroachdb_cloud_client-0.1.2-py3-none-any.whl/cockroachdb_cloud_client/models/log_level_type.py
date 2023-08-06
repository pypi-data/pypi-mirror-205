from enum import Enum


class LogLevelType(str, Enum):
    ERROR = "ERROR"
    FATAL = "FATAL"
    UNSPECIFIED = "UNSPECIFIED"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return str(self.value)
