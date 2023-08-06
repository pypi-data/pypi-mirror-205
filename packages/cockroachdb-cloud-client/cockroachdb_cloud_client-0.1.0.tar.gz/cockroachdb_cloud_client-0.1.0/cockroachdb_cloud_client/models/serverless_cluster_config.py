from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_limits import UsageLimits


T = TypeVar("T", bound="ServerlessClusterConfig")


@attr.s(auto_attribs=True)
class ServerlessClusterConfig:
    """
    Attributes:
        routing_id (str): routing_id is used to identify the cluster in a connection string.
        spend_limit (Union[Unset, int]): spend_limit is the maximum monthly charge for a cluster, in US cents. We
            recommend using usage_limits instead, since spend_limit will be deprecated
            in the future.
        usage_limits (Union[Unset, UsageLimits]):
    """

    routing_id: str
    spend_limit: Union[Unset, int] = UNSET
    usage_limits: Union[Unset, "UsageLimits"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        routing_id = self.routing_id
        spend_limit = self.spend_limit
        usage_limits: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.usage_limits, Unset):
            usage_limits = self.usage_limits.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "routing_id": routing_id,
            }
        )
        if spend_limit is not UNSET:
            field_dict["spend_limit"] = spend_limit
        if usage_limits is not UNSET:
            field_dict["usage_limits"] = usage_limits

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.usage_limits import UsageLimits

        d = src_dict.copy()
        routing_id = d.pop("routing_id")

        spend_limit = d.pop("spend_limit", UNSET)

        _usage_limits = d.pop("usage_limits", UNSET)
        usage_limits: Union[Unset, UsageLimits]
        if isinstance(_usage_limits, Unset):
            usage_limits = UNSET
        else:
            usage_limits = UsageLimits.from_dict(_usage_limits)

        serverless_cluster_config = cls(
            routing_id=routing_id,
            spend_limit=spend_limit,
            usage_limits=usage_limits,
        )

        serverless_cluster_config.additional_properties = d
        return serverless_cluster_config

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
