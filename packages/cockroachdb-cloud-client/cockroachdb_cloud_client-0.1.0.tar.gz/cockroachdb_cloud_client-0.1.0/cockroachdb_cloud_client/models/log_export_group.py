from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.log_level_type import LogLevelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogExportGroup")


@attr.s(auto_attribs=True)
class LogExportGroup:
    """LogExportGroup contains an export configuration for a single
    log group which can route logs for a subset of CRDB channels.

        Attributes:
            channels (List[str]): channels is a list of CRDB log channels to include in this
                group.
            log_name (str): log_name is the name of the group, reflected in the log sink.
            min_level (Union[Unset, LogLevelType]):  - UNSPECIFIED: The unspecified log level includes all logs.
                 - WARNING: The WARNING severity is used for situations which may require
                special handling, where normal operation is expected to resume
                automatically.
                 - ERROR: The ERROR severity is used for situations that require special
                handling, where normal operation could not proceed as expected.
                Other operations can continue mostly unaffected.
                 - FATAL: The FATAL severity is used for situations that require an
                immediate, hard server shutdown. A report is also sent to
                telemetry if telemetry is enabled.
            redact (Union[Unset, bool]): redact is a boolean that governs whether this log group
                should aggregate redacted logs. Redaction settings will
                inherit from the cluster log export defaults if unset.
    """

    channels: List[str]
    log_name: str
    min_level: Union[Unset, LogLevelType] = UNSET
    redact: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels = self.channels

        log_name = self.log_name
        min_level: Union[Unset, str] = UNSET
        if not isinstance(self.min_level, Unset):
            min_level = self.min_level.value

        redact = self.redact

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channels": channels,
                "log_name": log_name,
            }
        )
        if min_level is not UNSET:
            field_dict["min_level"] = min_level
        if redact is not UNSET:
            field_dict["redact"] = redact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channels = cast(List[str], d.pop("channels"))

        log_name = d.pop("log_name")

        _min_level = d.pop("min_level", UNSET)
        min_level: Union[Unset, LogLevelType]
        if isinstance(_min_level, Unset):
            min_level = UNSET
        else:
            min_level = LogLevelType(_min_level)

        redact = d.pop("redact", UNSET)

        log_export_group = cls(
            channels=channels,
            log_name=log_name,
            min_level=min_level,
            redact=redact,
        )

        log_export_group.additional_properties = d
        return log_export_group

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
