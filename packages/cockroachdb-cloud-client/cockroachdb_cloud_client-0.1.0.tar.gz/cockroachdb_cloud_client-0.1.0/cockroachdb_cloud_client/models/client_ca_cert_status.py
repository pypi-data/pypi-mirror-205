from enum import Enum


class ClientCACertStatus(str, Enum):
    FAILED = "FAILED"
    IS_SET = "IS_SET"
    NOT_SET = "NOT_SET"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)
