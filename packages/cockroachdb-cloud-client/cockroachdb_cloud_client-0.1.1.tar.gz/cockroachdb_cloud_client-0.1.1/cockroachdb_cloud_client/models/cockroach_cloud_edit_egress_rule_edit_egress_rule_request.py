from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CockroachCloudEditEgressRuleEditEgressRuleRequest")


@attr.s(auto_attribs=True)
class CockroachCloudEditEgressRuleEditEgressRuleRequest:
    """EditEgressRuleRequest is the input message to the EditEgressRule RPC.

    Example:
        {'cluster_id': '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'ports': [443, 80], 'rule_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa'}

    Attributes:
        description (Union[Unset, str]): description is text that serves to document the rules purpose.
        destination (Union[Unset, str]): destination is a CIDR range or fully-qualified domain name to which
            outgoing traffic should be allowed. This field is required.
        idempotency_key (Union[Unset, str]): idempotency_key uniquely identifies this request. If not set, it will be
            set by the server.
        paths (Union[Unset, List[str]]): paths are the allowed URL paths. If empty, all paths are allowed. Only
            valid if Type="FQDN".
        ports (Union[Unset, List[int]]): ports are the allowed ports for TCP protocol. If empty, all ports are
            allowed.
        type (Union[Unset, str]): type is the destination type of this rule. Example values are
            FQDN or CIDR. This field is required.
    """

    description: Union[Unset, str] = UNSET
    destination: Union[Unset, str] = UNSET
    idempotency_key: Union[Unset, str] = UNSET
    paths: Union[Unset, List[str]] = UNSET
    ports: Union[Unset, List[int]] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        destination = self.destination
        idempotency_key = self.idempotency_key
        paths: Union[Unset, List[str]] = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths

        ports: Union[Unset, List[int]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = self.ports

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if destination is not UNSET:
            field_dict["destination"] = destination
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if paths is not UNSET:
            field_dict["paths"] = paths
        if ports is not UNSET:
            field_dict["ports"] = ports
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        destination = d.pop("destination", UNSET)

        idempotency_key = d.pop("idempotency_key", UNSET)

        paths = cast(List[str], d.pop("paths", UNSET))

        ports = cast(List[int], d.pop("ports", UNSET))

        type = d.pop("type", UNSET)

        cockroach_cloud_edit_egress_rule_edit_egress_rule_request = cls(
            description=description,
            destination=destination,
            idempotency_key=idempotency_key,
            paths=paths,
            ports=ports,
            type=type,
        )

        cockroach_cloud_edit_egress_rule_edit_egress_rule_request.additional_properties = d
        return cockroach_cloud_edit_egress_rule_edit_egress_rule_request

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
