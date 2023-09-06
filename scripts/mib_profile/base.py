import yaml

from scripts.mib_profile import config, entity, mib_util


def create_device_meta() -> entity.MetadataResource:
    fields = {
        "vendor": entity.MetadataField(value="yamaha"),
        "description": entity.MetadataField(symbol=entity.Symbol("1.3.6.1.2.1.1.1", "sysDescr")),
        "sys_object_id": entity.MetadataField(
            symbol=entity.Symbol("1.3.6.1.2.1.1.2", "sysObjectID")
        ),
        "model": entity.MetadataField(
            symbol=entity.Symbol(
                "1.3.6.1.2.1.1.1", "sysDescr", match_pattern=r"([^\s]+) ", match_value="$1"
            )
        ),
        "os_version": entity.MetadataField(
            symbols=[
                mib_util.find_mib_symbol(
                    "ysfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"
                ),
                mib_util.find_mib_symbol(
                    "yrfRevision", match_pattern=r"([^\s]+ Rev[\d.]+)", match_value="$1"
                ),
            ]
        ),
        "serial_number": entity.MetadataField(
            symbol=entity.Symbol("1.3.6.1.2.1.47.1.1.1.1.11.1", "entPhysicalSerialNum")
        ),
        "location": entity.MetadataField(symbol=entity.Symbol("1.3.6.1.2.1.1.6", "sysLocation")),
    }

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

    interface_tag = [
        entity.MetricTagConfig("interface", column=entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr")),
        entity.MetricTagConfig(
            "interface_idx",
            column=entity.Symbol("1.3.6.1.2.1.2.2.1.1", "ifIndex"),
        ),
    ]

    yaml.dump(
        entity.entity_to_dict(
            {
                "metadata": {
                    "device": create_device_meta(),
                    "interface": create_interface_meta(),
                },
                "metrics": [
                    entity.Symbol("1.3.6.1.2.1.2.1.0", "ifNumber"),
                    entity.TableMetricsConfig(
                        table=entity.Symbol("1.3.6.1.2.1.2.2", "ifTable"),
                        symbols=[
                            entity.Symbol("1.3.6.1.2.1.2.2.1.5", "ifSpeed"),
                            entity.Symbol("1.3.6.1.2.1.2.2.1.7", "ifAdminStatus"),
                            entity.Symbol("1.3.6.1.2.1.2.2.1.8", "ifOperStatus"),
                        ],
                        metric_tags=interface_tag,
                    ),
                    entity.TableMetricsConfig(
                        table=entity.Symbol("1.3.6.1.2.1.2.2", "ifTable"),
                        symbols=[
                            entity.Symbol("1.3.6.1.2.1.2.2.1.13", "ifInDiscards"),
                            entity.Symbol("1.3.6.1.2.1.2.2.1.14", "ifInErrors"),
                            entity.Symbol("1.3.6.1.2.1.2.2.1.19", "ifOutDiscards"),
                            entity.Symbol("1.3.6.1.2.1.2.2.1.20", "ifOutErrors"),
                        ],
                        metric_tags=interface_tag,
                        metric_type=entity.ProfileMetricType.monotonic_count_and_rate,
                    ),
                    entity.TableMetricsConfig(
                        table=entity.Symbol("1.3.6.1.2.1.2.2", "ifTable"),
                        symbols=[
                            entity.Symbol("1.3.6.1.2.1.2.2.1.9", "ifLastChange"),
                        ],
                        metric_tags=interface_tag,
                        metric_type=entity.ProfileMetricType.gauge,
                    ),
                    entity.TableMetricsConfig(
                        table=entity.Symbol(" 1.3.6.1.2.1.31.1.1", "ifXTable"),
                        symbols=[
                            entity.Symbol("1.3.6.1.2.1.31.1.1.1.4", "ifHCInOctets"),
                            entity.Symbol("1.3.6.1.2.1.31.1.1.1.10", "ifHCOutOctets"),
                        ],
                        metric_tags=interface_tag,
                        metric_type=entity.ProfileMetricType.monotonic_count_and_rate,
                    ),
                ],
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)
