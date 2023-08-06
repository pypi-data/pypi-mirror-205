from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.cluster_major_version_support_status_type import ClusterMajorVersionSupportStatusType

T = TypeVar("T", bound="ClusterMajorVersion")


@attr.s(auto_attribs=True)
class ClusterMajorVersion:
    """For more information about CockroachDB cluster version support, see
    https://www.cockroachlabs.com/docs/releases/release-support-policy.html

        Attributes:
            support_status (ClusterMajorVersionSupportStatusType):
            version (str):
    """

    support_status: ClusterMajorVersionSupportStatusType
    version: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        support_status = self.support_status.value

        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "support_status": support_status,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        support_status = ClusterMajorVersionSupportStatusType(d.pop("support_status"))

        version = d.pop("version")

        cluster_major_version = cls(
            support_status=support_status,
            version=version,
        )

        cluster_major_version.additional_properties = d
        return cluster_major_version

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
