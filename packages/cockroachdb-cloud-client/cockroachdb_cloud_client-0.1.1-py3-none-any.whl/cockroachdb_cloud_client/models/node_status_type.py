from enum import Enum


class NodeStatusType(str, Enum):
    LIVE = "LIVE"
    NOT_READY = "NOT_READY"

    def __str__(self) -> str:
        return str(self.value)
