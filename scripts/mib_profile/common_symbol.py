from scripts.mib_profile import entity


class IfTable:
    ifTable = entity.Symbol("1.3.6.1.2.1.2.2", "ifTable")
    ifIndex = entity.Symbol("1.3.6.1.2.1.2.2.1.1", "ifIndex")
    ifDescr = entity.Symbol("1.3.6.1.2.1.2.2.1.2", "ifDescr")
    ifAdminStatus = entity.Symbol("1.3.6.1.2.1.2.2.1.7", "ifAdminStatus")
    ifOperStatus = entity.Symbol("1.3.6.1.2.1.2.2.1.8", "ifOperStatus")
    ifSpeed = entity.Symbol("1.3.6.1.2.1.2.2.1.5", "ifSpeed")


class IfXTable:
    ifXTable = entity.Symbol("1.3.6.1.2.1.31.1.1", "ifAlias")
    ifName = entity.Symbol("1.3.6.1.2.1.31.1.1.1.1", "ifName")
    ifAlias = entity.Symbol("1.3.6.1.2.1.31.1.1.1.18", "ifAlias")


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
