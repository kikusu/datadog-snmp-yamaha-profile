import yaml

from scripts.mib_profile import config, entity, mib_util


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
                ],
            }
        ),
        path.open("wt"),
        default_flow_style=False,
    )

    print("Save: ", path)
