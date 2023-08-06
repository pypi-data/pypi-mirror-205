from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.set_aws_endpoint_connection_status_type import SetAWSEndpointConnectionStatusType

T = TypeVar("T", bound="CockroachCloudSetAwsEndpointConnectionStateSetAwsEndpointConnectionStateRequest")


@attr.s(auto_attribs=True)
class CockroachCloudSetAwsEndpointConnectionStateSetAwsEndpointConnectionStateRequest:
    """
    Example:
        {'status': 'AVAILABLE'}

    Attributes:
        status (SetAWSEndpointConnectionStatusType):  - AVAILABLE: accept/verify the connection on the service side.
             - REJECTED: reject the connection on the service side.
    """

    status: SetAWSEndpointConnectionStatusType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = SetAWSEndpointConnectionStatusType(d.pop("status"))

        cockroach_cloud_set_aws_endpoint_connection_state_set_aws_endpoint_connection_state_request = cls(
            status=status,
        )

        cockroach_cloud_set_aws_endpoint_connection_state_set_aws_endpoint_connection_state_request.additional_properties = (
            d
        )
        return cockroach_cloud_set_aws_endpoint_connection_state_set_aws_endpoint_connection_state_request

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
