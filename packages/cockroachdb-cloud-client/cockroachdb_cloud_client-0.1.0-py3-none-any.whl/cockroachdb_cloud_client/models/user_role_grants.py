from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.built_in_role import BuiltInRole


T = TypeVar("T", bound="UserRoleGrants")


@attr.s(auto_attribs=True)
class UserRoleGrants:
    """
    Example:
        [{'name': 'CLUSTER_ADMIN', 'resource': {'id': 'example_cluster_id', 'type': 'CLUSTER'}}]

    Attributes:
        roles (List['BuiltInRole']):
        user_id (str):
    """

    roles: List["BuiltInRole"]
    user_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()

            roles.append(roles_item)

        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roles": roles,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.built_in_role import BuiltInRole

        d = src_dict.copy()
        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = BuiltInRole.from_dict(roles_item_data)

            roles.append(roles_item)

        user_id = d.pop("user_id")

        user_role_grants = cls(
            roles=roles,
            user_id=user_id,
        )

        user_role_grants.additional_properties = d
        return user_role_grants

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
