from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.currency_amount import CurrencyAmount


T = TypeVar("T", bound="InvoiceAdjustment")


@attr.s(auto_attribs=True)
class InvoiceAdjustment:
    """
    Attributes:
        amount (CurrencyAmount):
        name (str): name identifies the adjustment.
    """

    amount: "CurrencyAmount"
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount.to_dict()

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.currency_amount import CurrencyAmount

        d = src_dict.copy()
        amount = CurrencyAmount.from_dict(d.pop("amount"))

        name = d.pop("name")

        invoice_adjustment = cls(
            amount=amount,
            name=name,
        )

        invoice_adjustment.additional_properties = d
        return invoice_adjustment

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
