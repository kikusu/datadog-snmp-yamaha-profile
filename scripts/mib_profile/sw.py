import yaml

from scripts.mib_profile import base, common_symbol, config, entity, mib_util


def create_interface_meta() -> entity.MetadataResource:
    fields = {}
    fields["name"] = entity.MetadataField(symbol=common_symbol.IfTable.ifDescr)
    fields["description"] = entity.MetadataField(symbol=common_symbol.IfTable.ifDescr)

    fields["admin_status"] = entity.MetadataField(symbol=common_symbol.IfTable.ifAdminStatus)
    fields["oper_status"] = entity.MetadataField(symbol=common_symbol.IfTable.ifOperStatus)
    id_tags = [
        entity.MetadataTag(tag="interface", column=common_symbol.IfTable.ifDescr),
        entity.MetadataTag(
            "interface_idx",
            column=common_symbol.IfTable.ifIndex,
        ),
    ]

    return entity.MetadataResource(fields=fields, id_tags=id_tags)


def interface_metrics() -> list:
    interface_tag = [
        entity.MetricTagConfig("interface", column=common_symbol.IfTable.ifDescr),
        entity.MetricTagConfig(
            "interface_idx",
            column=common_symbol.IfTable.ifIndex,
        ),
        entity.MetricTagConfig(
            "interface_alias",
            column=common_symbol.IfXTable.ifAlias,
        ),
        common_symbol.CommonMetricTagConfig.interface_type,
    ]
    return [
        entity.TableMetricsConfig(
            table=common_symbol.IfTable.ifTable,
            symbols=[
                common_symbol.IfTable.ifSpeed,
                common_symbol.IfTable.ifAdminStatus,
                common_symbol.IfTable.ifOperStatus,
            ],
            metric_tags=interface_tag,
        ),
        entity.TableMetricsConfig(
            table=common_symbol.IfTable.ifTable,
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
            table=common_symbol.IfTable.ifTable,
            symbols=[
                entity.Symbol("1.3.6.1.2.1.2.2.1.9", "ifLastChange"),
            ],
            metric_tags=interface_tag,
            metric_type=entity.ProfileMetricType.monotonic_count,
        ),
        entity.TableMetricsConfig(
            table=entity.Symbol("1.3.6.1.2.1.31.1.1", "ifXTable"),
            symbols=[
                entity.Symbol("1.3.6.1.2.1.31.1.1.1.6", "ifHCInOctets"),
                entity.Symbol("1.3.6.1.2.1.31.1.1.1.10", "ifHCOutOctets"),
            ],
            metric_tags=interface_tag,
            metric_type=entity.ProfileMetricType.monotonic_count_and_rate,
        ),
        entity.TableMetricsConfig(
            table=entity.Symbol("1.3.6.1.2.1.31.1.1", "ifXTable"),
            symbols=[
                entity.Symbol("1.3.6.1.2.1.31.1.1.1.15", "ifHighSpeed"),
            ],
            metric_tags=interface_tag,
            metric_type=entity.ProfileMetricType.gauge,
        ),
    ]


def create_yamaha_sw():
    path = config.DST_DIR / "yamaha_sw.yaml"
    yaml.dump(
        entity.entity_to_dict(
            {
                "extends": [
                    "_yamaha_base.yml",
                ],
                "metadata": {
                    "interface": create_interface_meta(),
                },
                "sysobjectid": "1.3.6.1.4.1.1182.3.*",
                "metrics": [
                    entity.MetricsConfig(
                        symbol=mib_util.find_mib_symbol("yshCpuUtil1min", name="cpu.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=mib_util.find_mib_symbol("yshMemoryUtil", name="memory.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=mib_util.find_mib_symbol("yshMemorySize", name="memory.total")
                    ),
                    entity.Symbol("1.3.6.1.2.1.2.1.0", "ifNumber"),
                ]
                + interface_metrics(),
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)
