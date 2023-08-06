from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.network_visibility_type import NetworkVisibilityType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dedicated_cluster_create_specification_region_nodes import (
        DedicatedClusterCreateSpecificationRegionNodes,
    )
    from ..models.dedicated_hardware_create_specification import DedicatedHardwareCreateSpecification


T = TypeVar("T", bound="DedicatedClusterCreateSpecification")


@attr.s(auto_attribs=True)
class DedicatedClusterCreateSpecification:
    """
    Attributes:
        hardware (DedicatedHardwareCreateSpecification):
        region_nodes (DedicatedClusterCreateSpecificationRegionNodes): Region keys should match the cloud provider's
            zone code.
            For example, for Oregon, set region_name to "us-west2" for
            GCP and "us-west-2" for AWS. Values represent the node count.
        cockroach_version (Union[Unset, str]): The CockroachDB version for the cluster. The current version
            is used if omitted.
        network_visibility (Union[Unset, NetworkVisibilityType]):
        restrict_egress_traffic (Union[Unset, bool]): Preview: RestrictEgressTraffic if set, results in an egress
            traffic policy of
            default-deny at creation time.
    """

    hardware: "DedicatedHardwareCreateSpecification"
    region_nodes: "DedicatedClusterCreateSpecificationRegionNodes"
    cockroach_version: Union[Unset, str] = UNSET
    network_visibility: Union[Unset, NetworkVisibilityType] = UNSET
    restrict_egress_traffic: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hardware = self.hardware.to_dict()

        region_nodes = self.region_nodes.to_dict()

        cockroach_version = self.cockroach_version
        network_visibility: Union[Unset, str] = UNSET
        if not isinstance(self.network_visibility, Unset):
            network_visibility = self.network_visibility.value

        restrict_egress_traffic = self.restrict_egress_traffic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hardware": hardware,
                "region_nodes": region_nodes,
            }
        )
        if cockroach_version is not UNSET:
            field_dict["cockroach_version"] = cockroach_version
        if network_visibility is not UNSET:
            field_dict["network_visibility"] = network_visibility
        if restrict_egress_traffic is not UNSET:
            field_dict["restrict_egress_traffic"] = restrict_egress_traffic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dedicated_cluster_create_specification_region_nodes import (
            DedicatedClusterCreateSpecificationRegionNodes,
        )
        from ..models.dedicated_hardware_create_specification import DedicatedHardwareCreateSpecification

        d = src_dict.copy()
        hardware = DedicatedHardwareCreateSpecification.from_dict(d.pop("hardware"))

        region_nodes = DedicatedClusterCreateSpecificationRegionNodes.from_dict(d.pop("region_nodes"))

        cockroach_version = d.pop("cockroach_version", UNSET)

        _network_visibility = d.pop("network_visibility", UNSET)
        network_visibility: Union[Unset, NetworkVisibilityType]
        if isinstance(_network_visibility, Unset):
            network_visibility = UNSET
        else:
            network_visibility = NetworkVisibilityType(_network_visibility)

        restrict_egress_traffic = d.pop("restrict_egress_traffic", UNSET)

        dedicated_cluster_create_specification = cls(
            hardware=hardware,
            region_nodes=region_nodes,
            cockroach_version=cockroach_version,
            network_visibility=network_visibility,
            restrict_egress_traffic=restrict_egress_traffic,
        )

        dedicated_cluster_create_specification.additional_properties = d
        return dedicated_cluster_create_specification

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
