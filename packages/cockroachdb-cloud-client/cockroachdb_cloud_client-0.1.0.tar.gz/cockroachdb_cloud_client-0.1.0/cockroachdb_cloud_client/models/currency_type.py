from enum import Enum


class CurrencyType(str, Enum):
    CRDB_CLOUD_CREDITS = "CRDB_CLOUD_CREDITS"
    USD = "USD"

    def __str__(self) -> str:
        return str(self.value)
