from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_user_info_contains_information_about_a_person import (
        PersonUserInfoContainsInformationAboutAPerson,
    )


T = TypeVar("T", bound="GetPersonUsersByEmailResponse")


@attr.s(auto_attribs=True)
class GetPersonUsersByEmailResponse:
    """
    Attributes:
        user (Union[Unset, PersonUserInfoContainsInformationAboutAPerson]):
    """

    user: Union[Unset, "PersonUserInfoContainsInformationAboutAPerson"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.person_user_info_contains_information_about_a_person import (
            PersonUserInfoContainsInformationAboutAPerson,
        )

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, PersonUserInfoContainsInformationAboutAPerson]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = PersonUserInfoContainsInformationAboutAPerson.from_dict(_user)

        get_person_users_by_email_response = cls(
            user=user,
        )

        get_person_users_by_email_response.additional_properties = d
        return get_person_users_by_email_response

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
