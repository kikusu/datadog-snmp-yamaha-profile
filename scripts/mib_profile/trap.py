import yaml
from mib_profile import config, entity, mib_util


def find_mib_notification() -> dict:
    traps = {}
    mib_values_name = set()
    mib_module_names = set()
    mib_values = {}

    for f in config.SRC_DIR.glob("*.json"):
        mib = mib_util.load_mib_cache(f)
        for k, v in mib.items():
            if k in {"imports", "meta"}:
                continue
            if v["class"] == "notificationtype":
                traps[v["oid"]] = entity.TrapConfig(name=v["name"], mib=mib["meta"]["module"])
                mib_module_names.add(mib["meta"]["module"])

                for obj in v["objects"]:
                    if obj["object"] not in mib_values_name:
                        sym = mib_util.load_mib(obj["module"])[obj["object"]]

                        if sym["name"] == "yrIfWwanModAntLevel":
                            print(sym)

                        if sym.get("syntax", {}).get("constraints", {}).get("enumeration", {}):
                            mib_values[sym["oid"]] = entity.TrapVarsConfig(
                                name=sym["name"],
                                enum={
                                    v_: k_
                                    for k_, v_ in sym["syntax"]["constraints"][
                                        "enumeration"
                                    ].items()
                                },
                            )
                        else:
                            mib_values[sym["oid"]] = entity.TrapVarsConfig(name=sym["name"])
                        mib_values_name.add(obj["object"])

    return {
        "mibs": sorted(list(mib_module_names)),
        "traps": traps,
        "vars": mib_values,
    }


def create_yamaha_trap():
    path = config.DST_DIR / "yamaha_trap.yaml"
    yaml.dump(
        entity.entity_to_dict(find_mib_notification()),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)
