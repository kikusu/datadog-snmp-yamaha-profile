import dataclasses
from typing import Any


def entity_to_dict(var: Any):
    if hasattr(var, "to_json"):
        return var.to_json()
    elif isinstance(var, dict):
        return {k: entity_to_dict(v) for k, v in var.items() if v}
    elif isinstance(var, list):
        return [entity_to_dict(i) for i in var]
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


@dataclasses.dataclass
class MetadataField(JsonDataClass):
    symbol: Symbol | None = None
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
