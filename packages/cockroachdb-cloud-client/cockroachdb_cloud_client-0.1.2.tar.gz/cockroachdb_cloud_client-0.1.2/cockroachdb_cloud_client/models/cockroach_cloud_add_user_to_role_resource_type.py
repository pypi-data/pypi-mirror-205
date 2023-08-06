from enum import Enum


class CockroachCloudAddUserToRoleResourceType(str, Enum):
    CLUSTER = "CLUSTER"
    ORGANIZATION = "ORGANIZATION"

    def __str__(self) -> str:
        return str(self.value)
