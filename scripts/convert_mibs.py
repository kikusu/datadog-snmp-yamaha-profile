import pathlib
import shlex
import subprocess

if __name__ == "__main__":
    default_mib_path = (
        subprocess.run(shlex.split("net-snmp-config --default-mibdirs"), capture_output=True)
        .stdout.decode()
        .rstrip()
    )

    mibs = " ".join([str(i) for i in pathlib.Path("./src/yamaha-private-mib/").glob("*.mib.txt")])

    r = subprocess.run(
        shlex.split(
            "mibdump --destination-directory ./src/yamaha-private-mib-json/ "
            "--destination-format json "
            f"--mib-searcher {default_mib_path}:./src/yamaha-private-mib {mibs}"
        ),
    )
