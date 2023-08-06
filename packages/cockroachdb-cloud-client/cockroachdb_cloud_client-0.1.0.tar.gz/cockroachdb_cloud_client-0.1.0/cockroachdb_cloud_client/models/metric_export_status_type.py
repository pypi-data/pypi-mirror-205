from enum import Enum


class MetricExportStatusType(str, Enum):
    DISABLING = "DISABLING"
    ENABLED = "ENABLED"
    ENABLING = "ENABLING"
    ERROR = "ERROR"
    NOT_DEPLOYED = "NOT_DEPLOYED"

    def __str__(self) -> str:
        return str(self.value)
