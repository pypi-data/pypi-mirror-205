from enum import Enum


class ClusterMajorVersionSupportStatusType(str, Enum):
    PREVIEW = "PREVIEW"
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"

    def __str__(self) -> str:
        return str(self.value)
