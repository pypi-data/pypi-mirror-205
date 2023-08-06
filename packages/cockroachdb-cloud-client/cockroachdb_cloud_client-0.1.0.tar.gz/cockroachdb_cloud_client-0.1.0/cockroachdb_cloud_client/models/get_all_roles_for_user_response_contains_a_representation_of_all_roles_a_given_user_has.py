from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.built_in_role import BuiltInRole


T = TypeVar("T", bound="GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas")


@attr.s(auto_attribs=True)
class GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas:
    """
    Attributes:
        roles (Union[Unset, List['BuiltInRole']]):
    """

    roles: Union[Unset, List["BuiltInRole"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        roles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.to_dict()

                roles.append(roles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.built_in_role import BuiltInRole

        d = src_dict.copy()
        roles = []
        _roles = d.pop("roles", UNSET)
        for roles_item_data in _roles or []:
            roles_item = BuiltInRole.from_dict(roles_item_data)

            roles.append(roles_item)

        get_all_roles_for_user_response_contains_a_representation_of_all_roles_a_given_user_has = cls(
            roles=roles,
        )

        get_all_roles_for_user_response_contains_a_representation_of_all_roles_a_given_user_has.additional_properties = (
            d
        )
        return get_all_roles_for_user_response_contains_a_representation_of_all_roles_a_given_user_has

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
