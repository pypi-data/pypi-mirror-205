from enum import Enum


class PrivateEndpointServiceStatusType(str, Enum):
    AVAILABLE = "AVAILABLE"
    CREATE_FAILED = "CREATE_FAILED"
    CREATING = "CREATING"
    DELETE_FAILED = "DELETE_FAILED"
    DELETING = "DELETING"

    def __str__(self) -> str:
        return str(self.value)
