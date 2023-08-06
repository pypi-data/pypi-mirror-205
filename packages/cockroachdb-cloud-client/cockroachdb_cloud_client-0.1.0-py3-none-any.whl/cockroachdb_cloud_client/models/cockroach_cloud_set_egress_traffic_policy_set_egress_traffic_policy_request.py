from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest")


@attr.s(auto_attribs=True)
class CockroachCloudSetEgressTrafficPolicySetEgressTrafficPolicyRequest:
    """SetEgressTrafficPolicyRequest is the input for the SetEgressTrafficPolicy RPC.

    Attributes:
        allow_all (bool): allow_all, if true results in unrestricted egress traffic. If false, egress
            traffic is set to default-deny and is managed via the Egress Rule
            Management API.
        idempotency_key (Union[Unset, str]): idempotency_key uniquely identifies this request. If not set, it will be
            set by the server.
    """

    allow_all: bool
    idempotency_key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        allow_all = self.allow_all
        idempotency_key = self.idempotency_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allow_all": allow_all,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allow_all = d.pop("allow_all")

        idempotency_key = d.pop("idempotency_key", UNSET)

        cockroach_cloud_set_egress_traffic_policy_set_egress_traffic_policy_request = cls(
            allow_all=allow_all,
            idempotency_key=idempotency_key,
        )

        cockroach_cloud_set_egress_traffic_policy_set_egress_traffic_policy_request.additional_properties = d
        return cockroach_cloud_set_egress_traffic_policy_set_egress_traffic_policy_request

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
