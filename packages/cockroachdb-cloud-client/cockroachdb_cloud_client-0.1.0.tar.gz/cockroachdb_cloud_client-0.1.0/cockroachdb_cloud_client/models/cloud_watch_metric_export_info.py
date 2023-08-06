from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metric_export_status_type import MetricExportStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CloudWatchMetricExportInfo")


@attr.s(auto_attribs=True)
class CloudWatchMetricExportInfo:
    """
    Attributes:
        cluster_id (str):
        role_arn (str): role_arn is the IAM role used to upload metric segments to the
            target AWS account.
        log_group_name (Union[Unset, str]): log_group_name is the customized log group name.
        status (Union[Unset, MetricExportStatusType]):
        target_region (Union[Unset, str]): target_region specifies the specific AWS region that the metrics will
            be exported to.
        user_message (Union[Unset, str]):
    """

    cluster_id: str
    role_arn: str
    log_group_name: Union[Unset, str] = UNSET
    status: Union[Unset, MetricExportStatusType] = UNSET
    target_region: Union[Unset, str] = UNSET
    user_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id
        role_arn = self.role_arn
        log_group_name = self.log_group_name
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        target_region = self.target_region
        user_message = self.user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster_id": cluster_id,
                "role_arn": role_arn,
            }
        )
        if log_group_name is not UNSET:
            field_dict["log_group_name"] = log_group_name
        if status is not UNSET:
            field_dict["status"] = status
        if target_region is not UNSET:
            field_dict["target_region"] = target_region
        if user_message is not UNSET:
            field_dict["user_message"] = user_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("cluster_id")

        role_arn = d.pop("role_arn")

        log_group_name = d.pop("log_group_name", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, MetricExportStatusType]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = MetricExportStatusType(_status)

        target_region = d.pop("target_region", UNSET)

        user_message = d.pop("user_message", UNSET)

        cloud_watch_metric_export_info = cls(
            cluster_id=cluster_id,
            role_arn=role_arn,
            log_group_name=log_group_name,
            status=status,
            target_region=target_region,
            user_message=user_message,
        )

        cloud_watch_metric_export_info.additional_properties = d
        return cloud_watch_metric_export_info

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
