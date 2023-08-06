from enum import Enum


class ResourceTypeType(str, Enum):
    CLUSTER = "CLUSTER"
    ORGANIZATION = "ORGANIZATION"

    def __str__(self) -> str:
        return str(self.value)
