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


def find_mib(field: str) -> dict | None:
    for f in src_dir.glob("*.json"):
        mib = json.load(f.open())
        if field in mib:
            return mib[field]

    return None


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
    yaml.dump(
        entity.entity_to_dict(
            {
                "metadata": {
                    "device": create_device_meta(),
                    "interface": create_interface_meta(),
                    # "ip_addresses": create_ip_adresses_meta(),
                }
            }
        ),
        (dst_dir / "_yamaha_base.yml").open("wt"),
        default_flow_style=False,
    )


if __name__ == "__main__":
    print("src_dir: ", src_dir)
    print("dst_dir: ", dst_dir)

    create_base()
