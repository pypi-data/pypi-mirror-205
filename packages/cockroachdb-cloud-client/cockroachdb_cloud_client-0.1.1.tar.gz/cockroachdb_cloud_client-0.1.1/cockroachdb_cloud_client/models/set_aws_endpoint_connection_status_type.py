from enum import Enum


class SetAWSEndpointConnectionStatusType(str, Enum):
    AVAILABLE = "AVAILABLE"
    REJECTED = "REJECTED"

    def __str__(self) -> str:
        return str(self.value)
