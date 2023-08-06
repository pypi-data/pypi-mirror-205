from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.egress_rule import EgressRule


T = TypeVar("T", bound="DeleteEgressRuleResponse")


@attr.s(auto_attribs=True)
class DeleteEgressRuleResponse:
    """DeleteEgressRuleResponse is the output for the DeleteEgressRule RPC.

    Attributes:
        rule (Union[Unset, EgressRule]): EgressRule represents a network egress rule.
    """

    rule: Union[Unset, "EgressRule"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rule: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rule, Unset):
            rule = self.rule.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rule is not UNSET:
            field_dict["Rule"] = rule

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.egress_rule import EgressRule

        d = src_dict.copy()
        _rule = d.pop("Rule", UNSET)
        rule: Union[Unset, EgressRule]
        if isinstance(_rule, Unset):
            rule = UNSET
        else:
            rule = EgressRule.from_dict(_rule)

        delete_egress_rule_response = cls(
            rule=rule,
        )

        delete_egress_rule_response.additional_properties = d
        return delete_egress_rule_response

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
