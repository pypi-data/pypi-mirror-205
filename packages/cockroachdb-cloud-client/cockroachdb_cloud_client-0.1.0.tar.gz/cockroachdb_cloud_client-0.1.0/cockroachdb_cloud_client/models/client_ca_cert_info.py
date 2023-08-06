from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.client_ca_cert_status import ClientCACertStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ClientCACertInfo")


@attr.s(auto_attribs=True)
class ClientCACertInfo:
    """
    Attributes:
        status (Union[Unset, ClientCACertStatus]):  - UNKNOWN_STATUS: UNKNOWN should never be used; if it is used, it
            indicates a bug.
             - NOT_SET: NOT_SET indicates a client CA cert is not set on the cluster.
            New clusters won't have a client CA cert set.
             - IS_SET: IS_SET indicates a client CA cert is set on the cluster.
             - PENDING: PENDING indicates a client CA cert update is in flight on the cluster.
             - FAILED: FAILED indicates a client CA cert update was attempted, but failed.
        x509_pem_cert (Union[Unset, str]):
    """

    status: Union[Unset, ClientCACertStatus] = UNSET
    x509_pem_cert: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        x509_pem_cert = self.x509_pem_cert

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if x509_pem_cert is not UNSET:
            field_dict["x509_pem_cert"] = x509_pem_cert

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, ClientCACertStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ClientCACertStatus(_status)

        x509_pem_cert = d.pop("x509_pem_cert", UNSET)

        client_ca_cert_info = cls(
            status=status,
            x509_pem_cert=x509_pem_cert,
        )

        client_ca_cert_info.additional_properties = d
        return client_ca_cert_info

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
