import json
import pathlib

import yaml

from scripts import entity

root_dir = pathlib.Path(__file__).parent.parent.absolute()
dst_dir = root_dir / "dst"
src_dir = root_dir / "src" / "yamaha-private-mib-json"
dst_dir = pathlib.Path("/opt/datadog-agent/etc/conf.d/snmp.d/profiles/")

# References
# ----------
# https://pkg.go.dev/github.com/DataDog/datadog-agent/pkg/collector/corechecks/snmp/internal/checkconfig


def load_mib(mib_name: str, field: str | None = None) -> dict:
    mib = json.load((src_dir / f"{mib_name}.json").open())

    if field:
        return mib[field]
    return mib


def find_mib(field: str) -> dict:
    for f in src_dir.glob("*.json"):
        mib = json.load(f.open())
        if field in mib:
            return mib[field]

    raise KeyError(field)


def find_mib_symbol(field: str, **kwargs) -> entity.Symbol:
    for f in src_dir.glob("*.json"):
        mib = json.load(f.open())
        if field in mib:
            kwargs["OID"] = mib[field]["oid"]
            kwargs["name"] = kwargs.get("name", field)
            return entity.Symbol(**kwargs)

    raise KeyError(field)


def model_list() -> dict:
    return {
        v["oid"]: k.upper()
        for k, v in load_mib("YAMAHA-PRODUCTS-MIB").items()
        if v.get("class") == "objectidentity"
    }


def create_device_meta() -> entity.MetadataResource:
    fields = {}
    fields["vendor"] = entity.MetadataField(value="yamaha")

    fields["description"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.1.1", "sysDescr")
    )
    fields["sys_object_id"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.1.2", "sysObjectID")
    )
    fields["model"] = entity.MetadataField(
        symbol=entity.Symbol(
            "1.3.6.1.2.1.1.1", "sysDescr", match_pattern=r"([^\s]+) ", match_value="$1"
        )
    )
    fields["os_version"] = entity.MetadataField(
        symbols=[
            find_mib_symbol("ysfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"),
            find_mib_symbol("yrfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"),
        ]
    )

    return entity.MetadataResource(fields=fields)


def create_interface_meta() -> entity.MetadataResource:
    fields = {}
    fields["name"] = entity.MetadataField(symbol=entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr"))
    fields["description"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr")
    )

    fields["admin_status"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.2.2.1.7", "ifAdminStatus")
    )
    fields["oper_status"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.2.2.1.8", "ifOperStatus")
    )
    id_tags = [
        entity.MetadataTag(tag="interface", column=entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr"))
    ]

    return entity.MetadataResource(fields=fields, id_tags=id_tags)


def create_ip_adresses_meta() -> dict:
    fields = {}
    fields["if_index"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.4.20.1.2", "ipAdEntIfIndex")
    ).to_json()
    fields["netmask"] = entity.MetadataField(
        symbol=entity.Symbol("1.3.6.1.2.1.4.20.1.3", "ipAdEntNetMask")
    ).to_json()

    return {"fields": fields}


def create_base():
    path = dst_dir / "_yamaha_base.yml"
    yaml.dump(
        entity.entity_to_dict(
            {
                "metadata": {
                    "device": create_device_meta(),
                    "interface": create_interface_meta(),
                }
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)


def create_yamaha_rt():
    path = dst_dir / "yamaha_rt.yml"
    yaml.dump(
        entity.entity_to_dict(
            {
                "extends": [
                    "_yamaha_base.yml",
                    # "_generic-if.yaml"
                ],
                "sysobjectid": "1.3.6.1.4.1.1182.2.*",
                "metrics": [
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yrhCpuUtil1min", name="cpu.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yrhMemoryUtil", name="memory.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yrhMemorySize", name="memory.total")
                    ),
                    entity.TableMetricsConfig(
                        table=find_mib_symbol("yrhMultiCpuTable"),
                        symbols=[find_mib_symbol("yrhMultiCpuUtil1min")],
                        metric_tags=[entity.MetricTagConfig("cpu", index=1)],
                        metric_type=entity.ProfileMetricType.gauge,
                    ),
                ],
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)


def create_yamaha_sw():
    path = dst_dir / "yamaha_sw.yml"
    yaml.dump(
        entity.entity_to_dict(
            {
                "extends": [
                    "_yamaha_base.yml",
                    # "_generic-if.yaml"
                ],
                "sysobjectid": "1.3.6.1.4.1.1182.3.*",
                "metrics": [
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yshCpuUtil1min", name="cpu.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yshMemoryUtil", name="memory.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=find_mib_symbol("yshMemorySize", name="memory.total")
                    ),
                ],
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)


if __name__ == "__main__":
    print("src_dir: ", src_dir)
    print("dst_dir: ", dst_dir)

    create_base()
    create_yamaha_rt()
    create_yamaha_sw()
