from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.log_export_type import LogExportType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_export_group import LogExportGroup


T = TypeVar("T", bound="LogExportClusterSpecification")


@attr.s(auto_attribs=True)
class LogExportClusterSpecification:
    """LogExportClusterSpecification contains all the data necessary to
    configure log export for an individual cluster. Users would supply
    this data via the API and also receive it back when inspecting the
    state of their log export configuration.

        Attributes:
            auth_principal (Union[Unset, str]): auth_principal is either the AWS Role ARN that identifies a role
                that the cluster account can assume to write to CloudWatch or the
                GCP Project ID that the cluster service account has permissions to
                write to for cloud logging.
            groups (Union[Unset, List['LogExportGroup']]): groups is a collection of log group configurations to customize
                which CRDB channels get aggregated into different groups at the
                target sink. Unconfigured channels will be sent to the default
                locations via the settings above.
            log_name (Union[Unset, str]): log_name is an identifier for the logs in the customer's log sink.
            redact (Union[Unset, bool]): redact controls whether logs are redacted before forwarding to
                customer sinks. By default they are not redacted.
            region (Union[Unset, str]): region controls whether all logs are sent to a specific region in
                the customer sink. By default, logs will remain their region of
                origin depending on the cluster node's region.
            type (Union[Unset, LogExportType]): LogExportType encodes the cloud selection that we're exporting to
                along with the cloud logging platform.

                Currently, each cloud has a single logging platform.
    """

    auth_principal: Union[Unset, str] = UNSET
    groups: Union[Unset, List["LogExportGroup"]] = UNSET
    log_name: Union[Unset, str] = UNSET
    redact: Union[Unset, bool] = UNSET
    region: Union[Unset, str] = UNSET
    type: Union[Unset, LogExportType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auth_principal = self.auth_principal
        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        log_name = self.log_name
        redact = self.redact
        region = self.region
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auth_principal is not UNSET:
            field_dict["auth_principal"] = auth_principal
        if groups is not UNSET:
            field_dict["groups"] = groups
        if log_name is not UNSET:
            field_dict["log_name"] = log_name
        if redact is not UNSET:
            field_dict["redact"] = redact
        if region is not UNSET:
            field_dict["region"] = region
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_export_group import LogExportGroup

        d = src_dict.copy()
        auth_principal = d.pop("auth_principal", UNSET)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = LogExportGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        log_name = d.pop("log_name", UNSET)

        redact = d.pop("redact", UNSET)

        region = d.pop("region", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LogExportType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = LogExportType(_type)

        log_export_cluster_specification = cls(
            auth_principal=auth_principal,
            groups=groups,
            log_name=log_name,
            redact=redact,
            region=region,
            type=type,
        )

        log_export_cluster_specification.additional_properties = d
        return log_export_cluster_specification

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
