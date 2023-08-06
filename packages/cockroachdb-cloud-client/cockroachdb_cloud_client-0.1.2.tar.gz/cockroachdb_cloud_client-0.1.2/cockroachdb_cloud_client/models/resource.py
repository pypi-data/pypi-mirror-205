from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.resource_type_type import ResourceTypeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Resource")


@attr.s(auto_attribs=True)
class Resource:
    """
    Attributes:
        type (ResourceTypeType):
        id (Union[Unset, str]):
    """

    type: ResourceTypeType
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ResourceTypeType(d.pop("type"))

        id = d.pop("id", UNSET)

        resource = cls(
            type=type,
            id=id,
        )

        resource.additional_properties = d
        return resource

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
