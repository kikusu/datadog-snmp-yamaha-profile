import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
SRC_DIR = ROOT_DIR / ".." / "src" / "yamaha-private-mib-json"

# DST_DIR = ROOT_DIR / ".." / "dst"
DST_DIR = pathlib.Path("/opt/datadog-agent/etc/conf.d/snmp.d/profiles/")
