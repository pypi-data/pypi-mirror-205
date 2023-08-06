from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.log_export_type import LogExportType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_export_group import LogExportGroup


T = TypeVar("T", bound="CockroachCloudEnableLogExportEnableLogExportRequest")


@attr.s(auto_attribs=True)
class CockroachCloudEnableLogExportEnableLogExportRequest:
    """
    Example:
        {'auth_principal': 'my-gcp-project-id', 'groups': [{'channels': ['OPS', 'HEALTH'], 'log_name': 'devops',
            'min_level': 'WARNING'}], 'log_name': 'default', 'redact': True, 'type': 'GCP_CLOUD_LOGGING'}

    Attributes:
        auth_principal (str): auth_principal is either the AWS Role ARN that identifies a role
            that the cluster account can assume to write to CloudWatch or the
            GCP Project ID that the cluster service account has permissions to
            write to for cloud logging.
        log_name (str): log_name is an identifier for the logs in the customer's log sink.
        type (LogExportType): LogExportType encodes the cloud selection that we're exporting to
            along with the cloud logging platform.

            Currently, each cloud has a single logging platform.
        groups (Union[Unset, List['LogExportGroup']]): groups is a collection of log group configurations that allows
            the
            customer to define collections of CRDB log channels that are aggregated
            separately at the target sink.
        redact (Union[Unset, bool]): redact allows the customer to set a default redaction policy for
            logs before they are exported to the target sink. If a group config
            omits a redact flag and this one is set to `true`, then that group
            will receive redacted logs.
        region (Union[Unset, str]): region allows the customer to override the destination region for
            all logs for a cluster.
    """

    auth_principal: str
    log_name: str
    type: LogExportType
    groups: Union[Unset, List["LogExportGroup"]] = UNSET
    redact: Union[Unset, bool] = UNSET
    region: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auth_principal = self.auth_principal
        log_name = self.log_name
        type = self.type.value

        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        redact = self.redact
        region = self.region

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auth_principal": auth_principal,
                "log_name": log_name,
                "type": type,
            }
        )
        if groups is not UNSET:
            field_dict["groups"] = groups
        if redact is not UNSET:
            field_dict["redact"] = redact
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_export_group import LogExportGroup

        d = src_dict.copy()
        auth_principal = d.pop("auth_principal")

        log_name = d.pop("log_name")

        type = LogExportType(d.pop("type"))

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = LogExportGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        redact = d.pop("redact", UNSET)

        region = d.pop("region", UNSET)

        cockroach_cloud_enable_log_export_enable_log_export_request = cls(
            auth_principal=auth_principal,
            log_name=log_name,
            type=type,
            groups=groups,
            redact=redact,
            region=region,
        )

        cockroach_cloud_enable_log_export_enable_log_export_request.additional_properties = d
        return cockroach_cloud_enable_log_export_enable_log_export_request

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
