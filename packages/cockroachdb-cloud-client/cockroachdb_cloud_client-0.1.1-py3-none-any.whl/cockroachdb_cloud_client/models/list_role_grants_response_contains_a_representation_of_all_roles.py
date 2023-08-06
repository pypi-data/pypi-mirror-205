from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.keyset_pagination_response import KeysetPaginationResponse
    from ..models.user_role_grants import UserRoleGrants


T = TypeVar("T", bound="ListRoleGrantsResponseContainsARepresentationOfAllRoles")


@attr.s(auto_attribs=True)
class ListRoleGrantsResponseContainsARepresentationOfAllRoles:
    """
    Attributes:
        grants (Union[Unset, List['UserRoleGrants']]):
        pagination (Union[Unset, KeysetPaginationResponse]):
    """

    grants: Union[Unset, List["UserRoleGrants"]] = UNSET
    pagination: Union[Unset, "KeysetPaginationResponse"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        grants: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.grants, Unset):
            grants = []
            for grants_item_data in self.grants:
                grants_item = grants_item_data.to_dict()

                grants.append(grants_item)

        pagination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grants is not UNSET:
            field_dict["grants"] = grants
        if pagination is not UNSET:
            field_dict["pagination"] = pagination

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.keyset_pagination_response import KeysetPaginationResponse
        from ..models.user_role_grants import UserRoleGrants

        d = src_dict.copy()
        grants = []
        _grants = d.pop("grants", UNSET)
        for grants_item_data in _grants or []:
            grants_item = UserRoleGrants.from_dict(grants_item_data)

            grants.append(grants_item)

        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, KeysetPaginationResponse]
        if _pagination is None:
            pagination = None
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = KeysetPaginationResponse.from_dict(_pagination)

        list_role_grants_response_contains_a_representation_of_all_roles = cls(
            grants=grants,
            pagination=pagination,
        )

        list_role_grants_response_contains_a_representation_of_all_roles.additional_properties = d
        return list_role_grants_response_contains_a_representation_of_all_roles

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
