import dataclasses


@dataclasses.dataclass
class JsonDataClass:
    field_name = ""

    def to_json(self):
        return {self.field_name: {k: v for k, v in dataclasses.asdict(self).items() if v}}


@dataclasses.dataclass
class Symbol(JsonDataClass):
    field_name = "symbol"

    OID: str
    name: str
    mapping: dict[str, str] | None = None
