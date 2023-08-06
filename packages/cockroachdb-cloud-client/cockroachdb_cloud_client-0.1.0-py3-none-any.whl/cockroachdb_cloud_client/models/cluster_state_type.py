from enum import Enum


class ClusterStateType(str, Enum):
    CREATED = "CREATED"
    CREATING = "CREATING"
    CREATION_FAILED = "CREATION_FAILED"
    DELETED = "DELETED"
    LOCKED = "LOCKED"

    def __str__(self) -> str:
        return str(self.value)
