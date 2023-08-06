from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="UsageLimits")


@attr.s(auto_attribs=True)
class UsageLimits:
    """
    Attributes:
        request_unit_limit (str): request_unit_limit is the maximum number of request units that the cluster
            can consume during the month. If this limit is exceeded, then the cluster
            is disabled until the limit is increased, or until the beginning of the
            next month when more free request units are granted. It is an error for
            this to be zero.
        storage_mib_limit (str): storage_mib_limit is the maximum number of Mebibytes of storage that the
            cluster can have at any time during the month. If this limit is exceeded,
            then the cluster is throttled; only one SQL connection is allowed at a
            time, with the expectation that it is used to delete data to reduce storage
            usage. It is an error for this to be zero.
    """

    request_unit_limit: str
    storage_mib_limit: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_unit_limit = self.request_unit_limit
        storage_mib_limit = self.storage_mib_limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_unit_limit": request_unit_limit,
                "storage_mib_limit": storage_mib_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_unit_limit = d.pop("request_unit_limit")

        storage_mib_limit = d.pop("storage_mib_limit")

        usage_limits = cls(
            request_unit_limit=request_unit_limit,
            storage_mib_limit=storage_mib_limit,
        )

        usage_limits.additional_properties = d
        return usage_limits

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
