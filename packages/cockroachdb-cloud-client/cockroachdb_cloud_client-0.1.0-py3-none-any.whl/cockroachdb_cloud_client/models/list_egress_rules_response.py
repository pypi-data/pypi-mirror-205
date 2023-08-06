from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.egress_rule import EgressRule
    from ..models.keyset_pagination_response import KeysetPaginationResponse


T = TypeVar("T", bound="ListEgressRulesResponse")


@attr.s(auto_attribs=True)
class ListEgressRulesResponse:
    """ListEgressRulesResponse is the output for the ListEgressRules RPC.

    Attributes:
        pagination (Union[Unset, KeysetPaginationResponse]):
        rules (Union[Unset, List['EgressRule']]): rules are the egress rules associated with the given CockroachDB
            cluster.
    """

    pagination: Union[Unset, "KeysetPaginationResponse"] = UNSET
    rules: Union[Unset, List["EgressRule"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pagination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        rules: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()

                rules.append(rules_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pagination is not UNSET:
            field_dict["pagination"] = pagination
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.egress_rule import EgressRule
        from ..models.keyset_pagination_response import KeysetPaginationResponse

        d = src_dict.copy()
        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, KeysetPaginationResponse]
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = KeysetPaginationResponse.from_dict(_pagination)

        rules = []
        _rules = d.pop("rules", UNSET)
        for rules_item_data in _rules or []:
            rules_item = EgressRule.from_dict(rules_item_data)

            rules.append(rules_item)

        list_egress_rules_response = cls(
            pagination=pagination,
            rules=rules,
        )

        list_egress_rules_response.additional_properties = d
        return list_egress_rules_response

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
