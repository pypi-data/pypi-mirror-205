from enum import Enum


class ClusterUpgradeStatusType(str, Enum):
    FINALIZED = "FINALIZED"
    MAJOR_UPGRADE_RUNNING = "MAJOR_UPGRADE_RUNNING"
    PENDING_FINALIZATION = "PENDING_FINALIZATION"
    ROLLBACK_RUNNING = "ROLLBACK_RUNNING"
    UPGRADE_AVAILABLE = "UPGRADE_AVAILABLE"

    def __str__(self) -> str:
        return str(self.value)
