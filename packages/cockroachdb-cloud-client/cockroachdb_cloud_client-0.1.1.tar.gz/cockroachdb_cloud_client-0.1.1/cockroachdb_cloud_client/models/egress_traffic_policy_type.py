from enum import Enum


class EgressTrafficPolicyType(str, Enum):
    ALLOW_ALL = "ALLOW_ALL"
    DEFAULT_DENY = "DEFAULT_DENY"
    ERROR = "ERROR"
    UNSPECIFIED = "UNSPECIFIED"
    UPDATING = "UPDATING"

    def __str__(self) -> str:
        return str(self.value)
