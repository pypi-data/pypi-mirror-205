from enum import Enum


class AWSEndpointConnectionStatusType(str, Enum):
    AVAILABLE = "AVAILABLE"
    DELETED = "DELETED"
    DELETING = "DELETING"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    PENDING_ACCEPTANCE = "PENDING_ACCEPTANCE"
    REJECTED = "REJECTED"

    def __str__(self) -> str:
        return str(self.value)
