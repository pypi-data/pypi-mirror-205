from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.currency_type import CurrencyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CurrencyAmount")


@attr.s(auto_attribs=True)
class CurrencyAmount:
    """
    Attributes:
        amount (Union[Unset, float]): amount is the quantity of currency. Internally, currency amounts are tracked
            and stored using an arbitrary-precision decimal representation, but are serialized
            as 64-bit floating point numbers. There may be minor rounding discrepancies
            when parsed as a 32-bit float.
        currency (Union[Unset, CurrencyType]):
    """

    amount: Union[Unset, float] = UNSET
    currency: Union[Unset, CurrencyType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        currency: Union[Unset, str] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        _currency = d.pop("currency", UNSET)
        currency: Union[Unset, CurrencyType]
        if _currency is None:
            currency = None
        if isinstance(_currency, Unset):
            currency = UNSET
        else:
            currency = CurrencyType(_currency)

        currency_amount = cls(
            amount=amount,
            currency=currency,
        )

        currency_amount.additional_properties = d
        return currency_amount

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
