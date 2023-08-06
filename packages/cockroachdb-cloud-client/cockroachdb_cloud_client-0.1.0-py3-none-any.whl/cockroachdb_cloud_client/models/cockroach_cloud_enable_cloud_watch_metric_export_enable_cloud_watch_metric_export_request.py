from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CockroachCloudEnableCloudWatchMetricExportEnableCloudWatchMetricExportRequest")


@attr.s(auto_attribs=True)
class CockroachCloudEnableCloudWatchMetricExportEnableCloudWatchMetricExportRequest:
    """
    Example:
        {'log_group_name': 'example', 'role_arn': 'arn:aws:iam::account:role/ExampleRole', 'target_region': 'us-east-1'}

    Attributes:
        role_arn (str): role_arn is the IAM role used to upload metric segments to the
            target AWS account.
        log_group_name (Union[Unset, str]): log_group_name is the customized log group name.
        target_region (Union[Unset, str]): target_region specifies the specific AWS region that the metrics will
            be exported to.
    """

    role_arn: str
    log_group_name: Union[Unset, str] = UNSET
    target_region: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role_arn = self.role_arn
        log_group_name = self.log_group_name
        target_region = self.target_region

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role_arn": role_arn,
            }
        )
        if log_group_name is not UNSET:
            field_dict["log_group_name"] = log_group_name
        if target_region is not UNSET:
            field_dict["target_region"] = target_region

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role_arn = d.pop("role_arn")

        log_group_name = d.pop("log_group_name", UNSET)

        target_region = d.pop("target_region", UNSET)

        cockroach_cloud_enable_cloud_watch_metric_export_enable_cloud_watch_metric_export_request = cls(
            role_arn=role_arn,
            log_group_name=log_group_name,
            target_region=target_region,
        )

        cockroach_cloud_enable_cloud_watch_metric_export_enable_cloud_watch_metric_export_request.additional_properties = (
            d
        )
        return cockroach_cloud_enable_cloud_watch_metric_export_enable_cloud_watch_metric_export_request

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
