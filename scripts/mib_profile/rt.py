import yaml

from scripts.mib_profile import config, entity, mib_util


def create_yamaha_rt():
    path = config.DST_DIR / "yamaha_rt.yml"
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
                        symbol=mib_util.find_mib_symbol("yrhCpuUtil1min", name="cpu.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=mib_util.find_mib_symbol("yrhMemoryUtil", name="memory.usage")
                    ),
                    entity.MetricsConfig(
                        symbol=mib_util.find_mib_symbol("yrhMemorySize", name="memory.total")
                    ),
                    entity.TableMetricsConfig(
                        table=mib_util.find_mib_symbol("yrhMultiCpuTable"),
                        symbols=[mib_util.find_mib_symbol("yrhMultiCpuUtil1min")],
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
