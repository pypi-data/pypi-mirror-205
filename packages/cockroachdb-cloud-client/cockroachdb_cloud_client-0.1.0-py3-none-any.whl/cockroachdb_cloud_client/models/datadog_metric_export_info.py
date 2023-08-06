from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.datadog_site_type import DatadogSiteType
from ..models.metric_export_status_type import MetricExportStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatadogMetricExportInfo")


@attr.s(auto_attribs=True)
class DatadogMetricExportInfo:
    """
    Attributes:
        cluster_id (str):
        site (DatadogSiteType):
        api_key (Union[Unset, str]): api_key is the last 4 digits of a Datadog API key.
        status (Union[Unset, MetricExportStatusType]):
        user_message (Union[Unset, str]):
    """

    cluster_id: str
    site: DatadogSiteType
    api_key: Union[Unset, str] = UNSET
    status: Union[Unset, MetricExportStatusType] = UNSET
    user_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id
        site = self.site.value

        api_key = self.api_key
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        user_message = self.user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster_id": cluster_id,
                "site": site,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if status is not UNSET:
            field_dict["status"] = status
        if user_message is not UNSET:
            field_dict["user_message"] = user_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("cluster_id")

        site = DatadogSiteType(d.pop("site"))

        api_key = d.pop("api_key", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, MetricExportStatusType]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = MetricExportStatusType(_status)

        user_message = d.pop("user_message", UNSET)

        datadog_metric_export_info = cls(
            cluster_id=cluster_id,
            site=site,
            api_key=api_key,
            status=status,
            user_message=user_message,
        )

        datadog_metric_export_info.additional_properties = d
        return datadog_metric_export_info

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
