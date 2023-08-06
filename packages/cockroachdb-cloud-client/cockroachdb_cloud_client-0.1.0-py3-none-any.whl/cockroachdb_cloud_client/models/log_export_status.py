from enum import Enum


class LogExportStatus(str, Enum):
    DISABLED = "DISABLED"
    DISABLE_FAILED = "DISABLE_FAILED"
    DISABLING = "DISABLING"
    ENABLED = "ENABLED"
    ENABLE_FAILED = "ENABLE_FAILED"
    ENABLING = "ENABLING"

    def __str__(self) -> str:
        return str(self.value)
