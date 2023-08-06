from enum import Enum


class CockroachCloudGetConnectionStringOs(str, Enum):
    LINUX = "LINUX"
    MAC = "MAC"
    WINDOWS = "WINDOWS"

    def __str__(self) -> str:
        return str(self.value)
