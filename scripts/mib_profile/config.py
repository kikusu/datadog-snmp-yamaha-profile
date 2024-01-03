import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
SRC_DIR = (ROOT_DIR / ".." / "src" / "yamaha-private-mib-json").resolve()

DST_DIR = (ROOT_DIR / ".." / "dst").resolve()
# mac dir
# DST_DIR = pathlib.Path("/opt/datadog-agent/etc/conf.d/snmp.d/profiles/")
