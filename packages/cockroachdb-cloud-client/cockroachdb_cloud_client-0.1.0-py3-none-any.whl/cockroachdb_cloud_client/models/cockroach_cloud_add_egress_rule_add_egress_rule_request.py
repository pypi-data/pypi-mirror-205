from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CockroachCloudAddEgressRuleAddEgressRuleRequest")


@attr.s(auto_attribs=True)
class CockroachCloudAddEgressRuleAddEgressRuleRequest:
    """AddEgressRuleRequest is the input for the rpc AddEgressRule().

    Example:
        {'cluster_id': '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'description': 'egress for GCP storage buckets',
            'destination': 'storage.googleapis.com', 'name': 'roach-buckets', 'paths': ['/customer-managed-bucket-1/*',
            '/customer-managed-bucket-2/*'], 'ports': [443, 80], 'type': 'FQDN'}

    Attributes:
        description (str): description is text that serves to document the rules purpose.
        destination (str): destination is the endpoint (or subnetwork if CIDR) to which traffic is
            allowed.
        name (str): name is the name of the egress rule.
        type (str): type classifies the Destination field. Valid types include: "FQDN",
            "CIDR".
        idempotency_key (Union[Unset, str]): idempotency_key uniquely identifies this request. If not set, it will be
            set by the server.
        paths (Union[Unset, List[str]]): paths are the allowed URL paths. If empty, all paths are allowed. Only
            valid if Type="FQDN".
        ports (Union[Unset, List[int]]): ports are the allowed ports for TCP protocol. If Empty, all ports are
            allowed.
    """

    description: str
    destination: str
    name: str
    type: str
    idempotency_key: Union[Unset, str] = UNSET
    paths: Union[Unset, List[str]] = UNSET
    ports: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        destination = self.destination
        name = self.name
        type = self.type
        idempotency_key = self.idempotency_key
        paths: Union[Unset, List[str]] = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths

        ports: Union[Unset, List[int]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = self.ports

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "destination": destination,
                "name": name,
                "type": type,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if paths is not UNSET:
            field_dict["paths"] = paths
        if ports is not UNSET:
            field_dict["ports"] = ports

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        destination = d.pop("destination")

        name = d.pop("name")

        type = d.pop("type")

        idempotency_key = d.pop("idempotency_key", UNSET)

        paths = cast(List[str], d.pop("paths", UNSET))

        ports = cast(List[int], d.pop("ports", UNSET))

        cockroach_cloud_add_egress_rule_add_egress_rule_request = cls(
            description=description,
            destination=destination,
            name=name,
            type=type,
            idempotency_key=idempotency_key,
            paths=paths,
            ports=ports,
        )

        cockroach_cloud_add_egress_rule_add_egress_rule_request.additional_properties = d
        return cockroach_cloud_add_egress_rule_add_egress_rule_request

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
