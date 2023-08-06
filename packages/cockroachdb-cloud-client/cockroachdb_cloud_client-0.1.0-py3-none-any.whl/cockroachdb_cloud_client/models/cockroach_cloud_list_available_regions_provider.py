from enum import Enum


class CockroachCloudListAvailableRegionsProvider(str, Enum):
    AWS = "AWS"
    GCP = "GCP"

    def __str__(self) -> str:
        return str(self.value)
