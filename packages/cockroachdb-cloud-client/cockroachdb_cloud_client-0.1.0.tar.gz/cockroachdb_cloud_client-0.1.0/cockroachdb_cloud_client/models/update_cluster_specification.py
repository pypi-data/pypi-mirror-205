from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cluster_upgrade_status_type import ClusterUpgradeStatusType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dedicated_cluster_update_specification import DedicatedClusterUpdateSpecification
    from ..models.serverless_cluster_update_specification import ServerlessClusterUpdateSpecification


T = TypeVar("T", bound="UpdateClusterSpecification")


@attr.s(auto_attribs=True)
class UpdateClusterSpecification:
    """Set `upgrade_status` to 'UPGRADE_RUNNING' to start an upgrade. Multi-node clusters will undergo a rolling upgrade
    and will remain available, but single-node clusters will be briefly unavailable while the upgrade takes place.
    Upgrades will be finalized automatically after 72 hours, or can be manually finalized by setting the value to
    'FINALIZED'. Before the cluster is finalized, it can be rolled back by setting the value to 'ROLLBACK_RUNNING'.
    Version upgrade operations cannot be performed simultaneously with other update operations.

        Example:
            {'dedicated': {'hardware': {'machine_spec': {'machine_type': 'n2-standard-8'}}, 'region_nodes': {'us-central1':
                5, 'us-west1': 3}}, 'upgrade_status': 'UPGRADE_RUNNING'}

        Attributes:
            dedicated (Union[Unset, DedicatedClusterUpdateSpecification]):
            serverless (Union[Unset, ServerlessClusterUpdateSpecification]):
            upgrade_status (Union[Unset, ClusterUpgradeStatusType]):  - FINALIZED: The cluster is running the latest
                available CockroachDB version, and all upgrades have been finalized.
                 - MAJOR_UPGRADE_RUNNING: An major version upgrade is currently in progress.
                 - UPGRADE_AVAILABLE: An upgrade is available. If preview builds are enabled for the parent organization, this
                could indicate that a preview upgrade is available.
                 - PENDING_FINALIZATION: An upgrade is complete, but pending finalization. Upgrades are automatically finalized
                after 72 hours. For more information, see https://www.cockroachlabs.com/docs/stable/upgrade-cockroach-
                version.html
                 - ROLLBACK_RUNNING: A rollback operation is currently in progress.
    """

    dedicated: Union[Unset, "DedicatedClusterUpdateSpecification"] = UNSET
    serverless: Union[Unset, "ServerlessClusterUpdateSpecification"] = UNSET
    upgrade_status: Union[Unset, ClusterUpgradeStatusType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dedicated: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dedicated, Unset):
            dedicated = self.dedicated.to_dict()

        serverless: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.serverless, Unset):
            serverless = self.serverless.to_dict()

        upgrade_status: Union[Unset, str] = UNSET
        if not isinstance(self.upgrade_status, Unset):
            upgrade_status = self.upgrade_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dedicated is not UNSET:
            field_dict["dedicated"] = dedicated
        if serverless is not UNSET:
            field_dict["serverless"] = serverless
        if upgrade_status is not UNSET:
            field_dict["upgrade_status"] = upgrade_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dedicated_cluster_update_specification import DedicatedClusterUpdateSpecification
        from ..models.serverless_cluster_update_specification import ServerlessClusterUpdateSpecification

        d = src_dict.copy()
        _dedicated = d.pop("dedicated", UNSET)
        dedicated: Union[Unset, DedicatedClusterUpdateSpecification]
        if isinstance(_dedicated, Unset):
            dedicated = UNSET
        else:
            dedicated = DedicatedClusterUpdateSpecification.from_dict(_dedicated)

        _serverless = d.pop("serverless", UNSET)
        serverless: Union[Unset, ServerlessClusterUpdateSpecification]
        if isinstance(_serverless, Unset):
            serverless = UNSET
        else:
            serverless = ServerlessClusterUpdateSpecification.from_dict(_serverless)

        _upgrade_status = d.pop("upgrade_status", UNSET)
        upgrade_status: Union[Unset, ClusterUpgradeStatusType]
        if isinstance(_upgrade_status, Unset):
            upgrade_status = UNSET
        else:
            upgrade_status = ClusterUpgradeStatusType(_upgrade_status)

        update_cluster_specification = cls(
            dedicated=dedicated,
            serverless=serverless,
            upgrade_status=upgrade_status,
        )

        update_cluster_specification.additional_properties = d
        return update_cluster_specification

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
