import yaml

from scripts.mib_profile import common_symbol, config, entity, mib_util


def interface_metrics() -> list:
    interface_tag = [
        entity.MetricTagConfig("interface", column=entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr")),
        entity.MetricTagConfig(
            "interface_idx",
            column=entity.Symbol("1.3.6.1.2.1.2.2.1.1", "ifIndex"),
        ),
        entity.MetricTagConfig(
            "interface_alias",
            column=entity.Symbol("1.3.6.1.2.1.31.1.1.1.18", "ifAlias"),
        ),
        common_symbol.CommonMetricTagConfig.interface_type,
        entity.MetricTagConfig("snmp_host", column=entity.Symbol("1.3.6.1.2.1.1.5.0", "sysName")),
    ]
    return [
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
    path = config.DST_DIR / "yamaha_sw.yml"
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
