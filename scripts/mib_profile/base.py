import yaml

from scripts.mib_profile import config, entity, mib_util


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
            mib_util.find_mib_symbol(
                "ysfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"
            ),
            mib_util.find_mib_symbol(
                "yrfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"
            ),
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


def create_base():
    path = config.DST_DIR / "_yamaha_base.yml"
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
