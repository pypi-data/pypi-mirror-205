import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.cloud_provider_type import CloudProviderType
from ..models.cluster_state_type import ClusterStateType
from ..models.cluster_status_type import ClusterStatusType
from ..models.cluster_upgrade_status_type import ClusterUpgradeStatusType
from ..models.egress_traffic_policy_type import EgressTrafficPolicyType
from ..models.network_visibility_type import NetworkVisibilityType
from ..models.plan_type import PlanType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cluster_config import ClusterConfig
    from ..models.region import Region


T = TypeVar("T", bound="Cluster")


@attr.s(auto_attribs=True)
class Cluster:
    """
    Example:
        {'account_id': '', 'cloud_provider': 'GCP', 'cockroach_version': 'v21.2.4', 'config': {'serverless':
            {'routing_id': 'example-cluster-1533', 'spend_limit': 0}}, 'created_at': '2022-03-22T20:23:11.285067Z',
            'creator_id': '7cde0cd9-0d8a-4008-8f90-45092ce8afc1', 'deleted_at': None, 'id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa', 'name': 'example-cluster', 'operation_status':
            'CLUSTER_STATUS_UNSPECIFIED', 'plan': 'SERVERLESS', 'regions': [{'name': 'us-central1', 'node_count': 0,
            'sql_dns': 'free-tier7.gcp-us-central1.crdb.io', 'ui_dns': ''}], 'state': 'CREATED', 'updated_at':
            '2022-03-22T20:23:11.879593Z', 'upgrade_status': 'USING_LATEST'}

    Attributes:
        cloud_provider (CloudProviderType):  - GCP: The Google Cloud Platform cloud provider.
             - AWS: The Amazon Web Services cloud provider.
        cockroach_version (str):
        config (ClusterConfig):
        creator_id (str):
        id (str):
        name (str):
        operation_status (ClusterStatusType):
        plan (PlanType):  - DEDICATED: A paid plan that offers dedicated hardware in any location.
             - CUSTOM: A plan option that is used for clusters whose machine configs are not
            supported in self-service. All INVOICE clusters are under this plan option.
             - SERVERLESS: A paid plan that runs on shared hardware and caps the users'
            maximum monthly spending to a user-specified (possibly 0) amount.
        regions (List['Region']):
        state (ClusterStateType):  - LOCKED: An exclusive operation is being performed on this cluster.
            Other operations should not proceed if they did not set a cluster into the LOCKED state.
        upgrade_status (ClusterUpgradeStatusType):  - FINALIZED: The cluster is running the latest available CockroachDB
            version, and all upgrades have been finalized.
             - MAJOR_UPGRADE_RUNNING: An major version upgrade is currently in progress.
             - UPGRADE_AVAILABLE: An upgrade is available. If preview builds are enabled for the parent organization, this
            could indicate that a preview upgrade is available.
             - PENDING_FINALIZATION: An upgrade is complete, but pending finalization. Upgrades are automatically finalized
            after 72 hours. For more information, see https://www.cockroachlabs.com/docs/stable/upgrade-cockroach-
            version.html
             - ROLLBACK_RUNNING: A rollback operation is currently in progress.
        account_id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, datetime.datetime]):
        egress_traffic_policy (Union[Unset, EgressTrafficPolicyType]):  - UNSPECIFIED: UNSPECIFIED signifies the egress
            traffic policy is unspecified.
             - ERROR: ERROR signifies there has been an internal server error during
            an update to the egress traffic policy.
             - ALLOW_ALL: ALLOW_ALL signifies all outbound connections from CockroachDB are allowed.
             - DEFAULT_DENY: DEFAULT_DENY signifies that CockroachDB can only initiate network
            connections to destinations explicitly allowed by the user or CockroachDB
            Cloud operators.
             - UPDATING: UPDATING signifies the egress traffic policy is updating.
        network_visibility (Union[Unset, NetworkVisibilityType]):
        sql_dns (Union[Unset, str]): sql_dns is the DNS name of SQL interface of the cluster.
        updated_at (Union[Unset, datetime.datetime]):
    """

    cloud_provider: CloudProviderType
    cockroach_version: str
    config: "ClusterConfig"
    creator_id: str
    id: str
    name: str
    operation_status: ClusterStatusType
    plan: PlanType
    regions: List["Region"]
    state: ClusterStateType
    upgrade_status: ClusterUpgradeStatusType
    account_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, datetime.datetime] = UNSET
    egress_traffic_policy: Union[Unset, EgressTrafficPolicyType] = UNSET
    network_visibility: Union[Unset, NetworkVisibilityType] = UNSET
    sql_dns: Union[Unset, str] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cloud_provider = self.cloud_provider.value

        cockroach_version = self.cockroach_version
        config = self.config.to_dict()

        creator_id = self.creator_id
        id = self.id
        name = self.name
        operation_status = self.operation_status.value

        plan = self.plan.value

        regions = []
        for regions_item_data in self.regions:
            regions_item = regions_item_data.to_dict()

            regions.append(regions_item)

        state = self.state.value

        upgrade_status = self.upgrade_status.value

        account_id = self.account_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        egress_traffic_policy: Union[Unset, str] = UNSET
        if not isinstance(self.egress_traffic_policy, Unset):
            egress_traffic_policy = self.egress_traffic_policy.value

        network_visibility: Union[Unset, str] = UNSET
        if not isinstance(self.network_visibility, Unset):
            network_visibility = self.network_visibility.value

        sql_dns = self.sql_dns
        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cloud_provider": cloud_provider,
                "cockroach_version": cockroach_version,
                "config": config,
                "creator_id": creator_id,
                "id": id,
                "name": name,
                "operation_status": operation_status,
                "plan": plan,
                "regions": regions,
                "state": state,
                "upgrade_status": upgrade_status,
            }
        )
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if egress_traffic_policy is not UNSET:
            field_dict["egress_traffic_policy"] = egress_traffic_policy
        if network_visibility is not UNSET:
            field_dict["network_visibility"] = network_visibility
        if sql_dns is not UNSET:
            field_dict["sql_dns"] = sql_dns
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cluster_config import ClusterConfig
        from ..models.region import Region

        d = src_dict.copy()
        cloud_provider = CloudProviderType(d.pop("cloud_provider"))

        cockroach_version = d.pop("cockroach_version")

        config = ClusterConfig.from_dict(d.pop("config"))

        creator_id = d.pop("creator_id")

        id = d.pop("id")

        name = d.pop("name")

        operation_status = ClusterStatusType(d.pop("operation_status"))

        plan = PlanType(d.pop("plan"))

        regions = []
        _regions = d.pop("regions")
        for regions_item_data in _regions:
            regions_item = Region.from_dict(regions_item_data)

            regions.append(regions_item)

        state = ClusterStateType(d.pop("state"))

        upgrade_status = ClusterUpgradeStatusType(d.pop("upgrade_status"))

        account_id = d.pop("account_id", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _deleted_at = d.pop("deleted_at", UNSET)
        deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)

        _egress_traffic_policy = d.pop("egress_traffic_policy", UNSET)
        egress_traffic_policy: Union[Unset, EgressTrafficPolicyType]
        if isinstance(_egress_traffic_policy, Unset):
            egress_traffic_policy = UNSET
        else:
            egress_traffic_policy = EgressTrafficPolicyType(_egress_traffic_policy)

        _network_visibility = d.pop("network_visibility", UNSET)
        network_visibility: Union[Unset, NetworkVisibilityType]
        if isinstance(_network_visibility, Unset):
            network_visibility = UNSET
        else:
            network_visibility = NetworkVisibilityType(_network_visibility)

        sql_dns = d.pop("sql_dns", UNSET)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        cluster = cls(
            cloud_provider=cloud_provider,
            cockroach_version=cockroach_version,
            config=config,
            creator_id=creator_id,
            id=id,
            name=name,
            operation_status=operation_status,
            plan=plan,
            regions=regions,
            state=state,
            upgrade_status=upgrade_status,
            account_id=account_id,
            created_at=created_at,
            deleted_at=deleted_at,
            egress_traffic_policy=egress_traffic_policy,
            network_visibility=network_visibility,
            sql_dns=sql_dns,
            updated_at=updated_at,
        )

        cluster.additional_properties = d
        return cluster

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
