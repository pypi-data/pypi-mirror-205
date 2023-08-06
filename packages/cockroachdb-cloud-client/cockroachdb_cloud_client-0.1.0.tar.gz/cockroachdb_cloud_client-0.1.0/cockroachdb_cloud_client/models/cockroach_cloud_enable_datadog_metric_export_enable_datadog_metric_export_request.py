from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.datadog_site_type import DatadogSiteType

T = TypeVar("T", bound="CockroachCloudEnableDatadogMetricExportEnableDatadogMetricExportRequest")


@attr.s(auto_attribs=True)
class CockroachCloudEnableDatadogMetricExportEnableDatadogMetricExportRequest:
    """
    Example:
        {'api_key': 'datadog_api_key', 'site': 'US1'}

    Attributes:
        api_key (str): api_key is a Datadog API key.
        site (DatadogSiteType):
    """

    api_key: str
    site: DatadogSiteType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api_key = self.api_key
        site = self.site.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_key": api_key,
                "site": site,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_key = d.pop("api_key")

        site = DatadogSiteType(d.pop("site"))

        cockroach_cloud_enable_datadog_metric_export_enable_datadog_metric_export_request = cls(
            api_key=api_key,
            site=site,
        )

        cockroach_cloud_enable_datadog_metric_export_enable_datadog_metric_export_request.additional_properties = d
        return cockroach_cloud_enable_datadog_metric_export_enable_datadog_metric_export_request

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
