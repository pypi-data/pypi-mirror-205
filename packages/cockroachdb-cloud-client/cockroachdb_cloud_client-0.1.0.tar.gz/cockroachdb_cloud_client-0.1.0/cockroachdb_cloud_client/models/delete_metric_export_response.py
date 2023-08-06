from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metric_export_status_type import MetricExportStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteMetricExportResponse")


@attr.s(auto_attribs=True)
class DeleteMetricExportResponse:
    """
    Attributes:
        cluster_id (str):
        status (Union[Unset, MetricExportStatusType]):
    """

    cluster_id: str
    status: Union[Unset, MetricExportStatusType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster_id": cluster_id,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("cluster_id")

        _status = d.pop("status", UNSET)
        status: Union[Unset, MetricExportStatusType]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = MetricExportStatusType(_status)

        delete_metric_export_response = cls(
            cluster_id=cluster_id,
            status=status,
        )

        delete_metric_export_response.additional_properties = d
        return delete_metric_export_response

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
