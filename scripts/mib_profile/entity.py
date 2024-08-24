import dataclasses
import enum
from typing import Any


def entity_to_dict(var: Any):
    if hasattr(var, "to_json"):
        return var.to_json()
    elif isinstance(var, dict):
        return {k: entity_to_dict(v) for k, v in var.items() if v}
    elif isinstance(var, list):
        return [entity_to_dict(i) for i in var]
    elif isinstance(var, enum.Enum):
        return var.value
    return var


@dataclasses.dataclass
class JsonDataClass:
    def to_json(self):
        return {k: entity_to_dict(var) for k, var in dataclasses.asdict(self).items() if var}


@dataclasses.dataclass
class Symbol(JsonDataClass):
    OID: str
    name: str
    match_pattern: str | None = None
    match_value: str | None = None
    scale_factor: float | None = None


@dataclasses.dataclass
class MetadataField(JsonDataClass):
    symbol: Symbol | None = None
    symbols: list[Symbol] | None = None
    value: str | None = None


@dataclasses.dataclass
class MetadataTag(JsonDataClass):
    tag: str
    column: Symbol  # todo: rename symbol
    mapping: dict[str, str] | None = None


@dataclasses.dataclass
class MetadataResource(JsonDataClass):
    fields: dict[str, MetadataField] | None = None
    id_tags: list | None = None


class ProfileMetricType(enum.Enum):
    gauge = "gauge"
    monotonic_count = "monotonic_count"
    monotonic_count_and_rate = "monotonic_count_and_rate"
    rate = "rate"
    flag_stream = "flag_stream"


@dataclasses.dataclass
class MetricsConfig(JsonDataClass):
    symbol: Symbol
    metric_type: ProfileMetricType | None = None


@dataclasses.dataclass
class MetricTagConfig(JsonDataClass):
    tag: str
    column: Symbol | None = None
    index: int | None = None
    mapping: dict[str, str] | None = None


@dataclasses.dataclass
class TableMetricsConfig(JsonDataClass):
    table: Symbol
    symbols: list[Symbol]
    metric_type: ProfileMetricType | None = None
    metric_tags: list[MetricTagConfig] | None = None


@dataclasses.dataclass
class TrapConfig(JsonDataClass):
    mib: str
    name: str


@dataclasses.dataclass
class TrapVarsConfig(JsonDataClass):
    name: str
    enum: dict | None = None
