from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cluster_major_version import ClusterMajorVersion
    from ..models.keyset_pagination_response import KeysetPaginationResponse


T = TypeVar("T", bound="ListMajorClusterVersionsResponse")


@attr.s(auto_attribs=True)
class ListMajorClusterVersionsResponse:
    """
    Attributes:
        versions (List['ClusterMajorVersion']):
        pagination (Union[Unset, KeysetPaginationResponse]):
    """

    versions: List["ClusterMajorVersion"]
    pagination: Union[Unset, "KeysetPaginationResponse"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()

            versions.append(versions_item)

        pagination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "versions": versions,
            }
        )
        if pagination is not UNSET:
            field_dict["pagination"] = pagination

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cluster_major_version import ClusterMajorVersion
        from ..models.keyset_pagination_response import KeysetPaginationResponse

        d = src_dict.copy()
        versions = []
        _versions = d.pop("versions")
        for versions_item_data in _versions:
            versions_item = ClusterMajorVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, KeysetPaginationResponse]
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = KeysetPaginationResponse.from_dict(_pagination)

        list_major_cluster_versions_response = cls(
            versions=versions,
            pagination=pagination,
        )

        list_major_cluster_versions_response.additional_properties = d
        return list_major_cluster_versions_response

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
