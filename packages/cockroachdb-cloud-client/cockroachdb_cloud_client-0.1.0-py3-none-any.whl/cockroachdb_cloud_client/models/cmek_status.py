from enum import Enum


class CMEKStatus(str, Enum):
    DISABLED = "DISABLED"
    DISABLE_FAILED = "DISABLE_FAILED"
    DISABLING = "DISABLING"
    ENABLED = "ENABLED"
    ENABLE_FAILED = "ENABLE_FAILED"
    ENABLING = "ENABLING"
    REVOKED = "REVOKED"
    REVOKE_FAILED = "REVOKE_FAILED"
    REVOKING = "REVOKING"
    ROTATE_FAILED = "ROTATE_FAILED"
    ROTATING = "ROTATING"

    def __str__(self) -> str:
        return str(self.value)
