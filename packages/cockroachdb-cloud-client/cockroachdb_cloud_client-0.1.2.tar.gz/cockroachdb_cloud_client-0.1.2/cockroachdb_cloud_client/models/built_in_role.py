from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.organization_user_role_type import OrganizationUserRoleType

if TYPE_CHECKING:
    from ..models.resource import Resource


T = TypeVar("T", bound="BuiltInRole")


@attr.s(auto_attribs=True)
class BuiltInRole:
    """
    Attributes:
        name (OrganizationUserRoleType):
        resource (Resource):
    """

    name: OrganizationUserRoleType
    resource: "Resource"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name.value

        resource = self.resource.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resource": resource,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resource import Resource

        d = src_dict.copy()
        name = OrganizationUserRoleType(d.pop("name"))

        resource = Resource.from_dict(d.pop("resource"))

        built_in_role = cls(
            name=name,
            resource=resource,
        )

        built_in_role.additional_properties = d
        return built_in_role

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
