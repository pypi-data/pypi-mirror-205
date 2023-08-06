from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_connection_string_response_params import GetConnectionStringResponseParams


T = TypeVar("T", bound="GetConnectionStringResponse")


@attr.s(auto_attribs=True)
class GetConnectionStringResponse:
    """
    Attributes:
        connection_string (Union[Unset, str]): connection_string contains the full connection string with parameters
            formatted inline.
        params (Union[Unset, GetConnectionStringResponseParams]): params contains a list of individual key parameters
            for generating nonstandard connection strings.
    """

    connection_string: Union[Unset, str] = UNSET
    params: Union[Unset, "GetConnectionStringResponseParams"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connection_string = self.connection_string
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connection_string is not UNSET:
            field_dict["connection_string"] = connection_string
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_connection_string_response_params import GetConnectionStringResponseParams

        d = src_dict.copy()
        connection_string = d.pop("connection_string", UNSET)

        _params = d.pop("params", UNSET)
        params: Union[Unset, GetConnectionStringResponseParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = GetConnectionStringResponseParams.from_dict(_params)

        get_connection_string_response = cls(
            connection_string=connection_string,
            params=params,
        )

        get_connection_string_response.additional_properties = d
        return get_connection_string_response

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
