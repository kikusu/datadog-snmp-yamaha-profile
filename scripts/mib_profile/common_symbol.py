from scripts.mib_profile import entity


class CommonMetricTagConfig:
    interface_type = entity.MetricTagConfig(
        "interface_type",
        column=entity.Symbol("1.3.6.1.2.1.2.2.1.3", "ifType"),
        mapping={
            "1": "other",
            "136": "l3ipvlan",
            "23": "ppp",
            "24": "softwareLoopback",
            "6": "ethernet-csmacd",
        },
    )
