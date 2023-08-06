import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EgressRule")


@attr.s(auto_attribs=True)
class EgressRule:
    """EgressRule represents a network egress rule.

    Attributes:
        cluster_id (str): cluster_id identifies the cluster to which this egress rule applies.
        crl_managed (bool): crl_managed indicates this egress rule is managed by CockroachDB Cloud
            services. This field is set by the server.
        description (str): description is a longer that serves to document the rules purpose.
        destination (str): destination is the endpoint (or subnetwork if CIDR) to which traffic is
            allowed.
        id (str): id uniquely identifies this egress rule.
        name (str): name is the name of the egress rule.
        state (str): state indicates the state of the egress rule.
        type (str): type classifies the destination field. Valid types include: "FQDN",
            "CIDR".
        created_at (Union[Unset, datetime.datetime]): created_at is the time at which the time at which the egress rule
            was
            created.
        paths (Union[Unset, List[str]]): paths are the allowed URL paths. Only valid if Type="FQDN".
        ports (Union[Unset, List[int]]): ports are the allowed ports for TCP protocol. If Empty, all ports are
            allowed.
    """

    cluster_id: str
    crl_managed: bool
    description: str
    destination: str
    id: str
    name: str
    state: str
    type: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    paths: Union[Unset, List[str]] = UNSET
    ports: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id
        crl_managed = self.crl_managed
        description = self.description
        destination = self.destination
        id = self.id
        name = self.name
        state = self.state
        type = self.type
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

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
                "cluster_id": cluster_id,
                "crl_managed": crl_managed,
                "description": description,
                "destination": destination,
                "id": id,
                "name": name,
                "state": state,
                "type": type,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if paths is not UNSET:
            field_dict["paths"] = paths
        if ports is not UNSET:
            field_dict["ports"] = ports

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("cluster_id")

        crl_managed = d.pop("crl_managed")

        description = d.pop("description")

        destination = d.pop("destination")

        id = d.pop("id")

        name = d.pop("name")

        state = d.pop("state")

        type = d.pop("type")

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        paths = cast(List[str], d.pop("paths", UNSET))

        ports = cast(List[int], d.pop("ports", UNSET))

        egress_rule = cls(
            cluster_id=cluster_id,
            crl_managed=crl_managed,
            description=description,
            destination=destination,
            id=id,
            name=name,
            state=state,
            type=type,
            created_at=created_at,
            paths=paths,
            ports=ports,
        )

        egress_rule.additional_properties = d
        return egress_rule

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
