SHELL := bash 
MIB_FILES := $(shell ls src/yamaha-private-mib/*.txt)
EMPTY :=
SPACE := $(EMPTY) $(EMPTY)
MIBS = $(subst  $(SPACE),:,$(MIB_FILES))

DEVICE_IP = 192.168.100.1

init:
	pip install -r requirements.txt

snmp:
	snmpwalk -v 2c -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) > snmp.txt

	snmpwalk -v 2c -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) .1.3.6.1.4.1.1182 >> snmp.txt

snmp_n:
	snmpwalk -v 2c -On -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) > snmp_n.txt

	snmpwalk -v 2c -On -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) .1.3.6.1.4.1.1182 >> snmp_n.txt

snmp_m: snmp_n snmp

snmpwalk:
	snmpwalk -v 2c -On -c public \
	-M $$(net-snmp-config --default-mibdirs):$$(pwd)/src/yamaha-private-mib \
	-m $(MIBS) \
	$(DEVICE_IP) $(TARGET)
