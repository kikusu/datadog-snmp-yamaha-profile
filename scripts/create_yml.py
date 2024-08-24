from scripts.mib_profile import base, config, rt, sw, trap

# References
# ----------
# https://pkg.go.dev/github.com/DataDog/datadog-agent/pkg/collector/corechecks/snmp/internal/checkconfig


if __name__ == "__main__":
    print("src_dir: ", config.SRC_DIR)
    print("dst_dir: ", config.DST_DIR)

    base.create_base()
    rt.create_yamaha_rt()
    sw.create_yamaha_sw()
    trap.create_yamaha_trap()
