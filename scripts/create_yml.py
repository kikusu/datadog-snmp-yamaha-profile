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


def load_mib(mib_name: str, field: str = None) -> dict:
    mib = json.load((src_dir / f"{mib_name}.json").open())

    if field:
        return mib[field]
    return mib


def find_mib(field: str) -> dict:
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


def create_device_meta() -> dict:
    field: dict[str, any] = {"vendor": {"value": "yamaha"}}

    field["description"] = entity.Symbol("1.3.6.1.2.1.1.1", "sysDescr").to_json()
    field["sys_object_id"] = entity.Symbol("1.3.6.1.2.1.1.2", "sysObjectID").to_json()
    field["model"] = entity.Symbol("1.3.6.1.2.1.1.2", "sysObjectID", mapping=model_list()).to_json()
    return {"field": field}


def create_interface_meta() -> dict:
    field = {}
    field["name"] = entity.Symbol("1.3.6.1.2.1.2.2.1.2", " ifDescr").to_json()
    field["admin_status"] = entity.Symbol("1.3.6.1.2.1.2.2.1.7", "ifAdminStatus").to_json()
    field["oper_status"] = entity.Symbol("1.3.6.1.2.1.2.2.1.8", "ifOperStatus").to_json()

    id_tags = [
        {"tag": "interface", "column": entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr").to_json()}
    ]

    return {"field": field, "id_tags": id_tags}


def create_base():
    yaml.dump(
        {
            "metadata": {
                "device": create_device_meta(),
                "interface": create_interface_meta(),
            }
        },
        (dst_dir / "_yamaha_base.yml").open("wt"),
        default_flow_style=False,
    )


if __name__ == "__main__":
    print("src_dir: ", src_dir)
    print("dst_dir: ", dst_dir)

    create_base()
