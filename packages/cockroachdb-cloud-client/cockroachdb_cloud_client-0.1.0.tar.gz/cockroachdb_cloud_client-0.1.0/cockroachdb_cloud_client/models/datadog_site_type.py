from enum import Enum


class DatadogSiteType(str, Enum):
    EU1 = "EU1"
    US1 = "US1"
    US1_GOV = "US1_GOV"
    US3 = "US3"
    US5 = "US5"

    def __str__(self) -> str:
        return str(self.value)
