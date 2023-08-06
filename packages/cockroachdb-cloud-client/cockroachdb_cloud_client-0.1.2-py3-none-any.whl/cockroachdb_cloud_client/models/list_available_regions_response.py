from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_provider_region import CloudProviderRegion
    from ..models.keyset_pagination_response import KeysetPaginationResponse


T = TypeVar("T", bound="ListAvailableRegionsResponse")


@attr.s(auto_attribs=True)
class ListAvailableRegionsResponse:
    """
    Attributes:
        regions (List['CloudProviderRegion']):
        pagination (Union[Unset, KeysetPaginationResponse]):
    """

    regions: List["CloudProviderRegion"]
    pagination: Union[Unset, "KeysetPaginationResponse"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        regions = []
        for regions_item_data in self.regions:
            regions_item = regions_item_data.to_dict()

            regions.append(regions_item)

        pagination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "regions": regions,
            }
        )
        if pagination is not UNSET:
            field_dict["pagination"] = pagination

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cloud_provider_region import CloudProviderRegion
        from ..models.keyset_pagination_response import KeysetPaginationResponse

        d = src_dict.copy()
        regions = []
        _regions = d.pop("regions")
        for regions_item_data in _regions:
            regions_item = CloudProviderRegion.from_dict(regions_item_data)

            regions.append(regions_item)

        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, KeysetPaginationResponse]

        if isinstance(_pagination, Unset) or not _pagination:
            pagination = UNSET
        else:
            pagination = KeysetPaginationResponse.from_dict(_pagination)

        list_available_regions_response = cls(
            regions=regions,
            pagination=pagination,
        )

        list_available_regions_response.additional_properties = d
        return list_available_regions_response

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
