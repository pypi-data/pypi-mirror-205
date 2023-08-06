from enum import Enum


class PlanType(str, Enum):
    CUSTOM = "CUSTOM"
    DEDICATED = "DEDICATED"
    SERVERLESS = "SERVERLESS"

    def __str__(self) -> str:
        return str(self.value)
