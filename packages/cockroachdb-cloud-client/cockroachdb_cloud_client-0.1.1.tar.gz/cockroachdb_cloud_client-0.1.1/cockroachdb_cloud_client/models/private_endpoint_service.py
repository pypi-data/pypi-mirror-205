from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.cloud_provider_type import CloudProviderType
from ..models.private_endpoint_service_status_type import PrivateEndpointServiceStatusType

if TYPE_CHECKING:
    from ..models.aws_private_link_service_detail import AWSPrivateLinkServiceDetail


T = TypeVar("T", bound="PrivateEndpointService")


@attr.s(auto_attribs=True)
class PrivateEndpointService:
    """
    Attributes:
        aws (AWSPrivateLinkServiceDetail):
        cloud_provider (CloudProviderType):  - GCP: The Google Cloud Platform cloud provider.
             - AWS: The Amazon Web Services cloud provider.
        region_name (str): region_name is the cloud provider region name (i.e. us-east-1).
        status (PrivateEndpointServiceStatusType):
    """

    aws: "AWSPrivateLinkServiceDetail"
    cloud_provider: CloudProviderType
    region_name: str
    status: PrivateEndpointServiceStatusType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aws = self.aws.to_dict()

        cloud_provider = self.cloud_provider.value

        region_name = self.region_name
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aws": aws,
                "cloud_provider": cloud_provider,
                "region_name": region_name,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.aws_private_link_service_detail import AWSPrivateLinkServiceDetail

        d = src_dict.copy()
        aws = AWSPrivateLinkServiceDetail.from_dict(d.pop("aws"))

        cloud_provider = CloudProviderType(d.pop("cloud_provider"))

        region_name = d.pop("region_name")

        status = PrivateEndpointServiceStatusType(d.pop("status"))

        private_endpoint_service = cls(
            aws=aws,
            cloud_provider=cloud_provider,
            region_name=region_name,
            status=status,
        )

        private_endpoint_service.additional_properties = d
        return private_endpoint_service

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
