SHELL := bash 
MIB_FILES := $(shell ls src/yamaha-private-mib/*.txt)
EMPTY :=
SPACE := $(EMPTY) $(EMPTY)
MIBS = $(subst  $(SPACE),:,$(MIB_FILES))

DEVICE_IP = 192.168.100.1
export PYTHONPATH := $(shell pwd)

init:
	pip install -r requirements.txt

snmp:
	snmpwalk -v 2c -c public -O bentU \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) > snmp.txt

snmp_n:
	snmpwalk -v 2c -On -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) > snmp_n.txt

snmp_m: snmp_n snmp

snmpwalk:
	snmpwalk -v 2c -O bentU -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) $(TARGET)

build:
	python scripts/create_yml.py;

test:
	datadog-agent check snmp --table --check-rate -l debug
