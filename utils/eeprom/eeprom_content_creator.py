from datetime import datetime
import json
import sys
import re
import pickle

state_file = "/tmp/eeprom.pkl"

def menu(options,title):
    while True:
        for i, dl in enumerate(options):
            print(f"{i}) {dl}")
        try:
            dln = int(input(title))
            if dln <= len(options):
                return options[dln]
            else:
                print("Option not found!")
        except Exception as e:
            print("exception", e)

print("Welcome to eeprom content creator!")
answer = input("Creat eeprom content? (y/n)").lower()
if answer != "y":
    sys.exit(1)

data_loggers = ["NDAS-8436N", "NDAS-8426N", "NDAS-8446 RT", "CME-4211RT"]  # dataloggers of R-Sensors
adc_boards = ["NDAS-8026 v1.4", "NDAS-8016 v1.2.1", "NDAS-8424 v1.1"]  # ADC of dataloggers
hws = ["NDAS-8046 v1.3", "NDAS-8044 v1.2.1",
       "NDAS-8046 v1.2", adc_boards[2]]  # hardwares of dataloggers

date = datetime.now().strftime('%Y-%m-%d')
license_type = { "NDAS-8436N" : "ndas8436n_6ch", "NDAS-8426N" : "ndas8426n_6ch", "NDAS-8446 RT" : "ndas_rt_no_adc", "CME-4211RT" : "ndas8426n_6ch" }
data_logger = menu(data_loggers, "Choose datalogger type: ")
if data_logger == "NDAS-8446 RT":
    adc_board = None
elif data_logger == "CME-4211RT":
    adc_board = adc_boards[2]
else:
    adc_board = menu(adc_boards, "Choose ADC board: ")
if data_logger == "CME-4211RT":
   hardware = hws[3]
else:
    hardware = menu(hws, "Choose hardware version: ")

hw_version = hardware[hardware.index("v")+1:]
while True:
    serial_number = input("Enter serial number (Example: RS005751): RS00")
    sn_pattern = r"^\d{4}$"
    if re.match(sn_pattern, serial_number):
        serial_number = "RS00" + serial_number
        break
    else:
        print(f"wrong serial number RS00{serial_number}")

eeprom_content = {
    "boards": {"adc_boards": [adc_board] if adc_board is not None else [],
               "motherboard":  hardware,
               "sbc_board": "bb_green",
               **({"vcxo": "tg2016_16384"} if data_logger != "NDAS-8446 RT" else {})
               },
    "comment": "",
    "hw": ["Port 1"] + (["Port 2", "NDAS Port 1", "NDAS Port 2", "Slot 1"] if data_logger == "NDAS-8446 RT" else []) +
    (["lsm303agr"] if data_logger == "CME-4211RT" else ["5V output", "NDAS_ports_Vin"])+
    ["HTS221",
     "m41t81s",
     "MAX-M8Q"
     ],
    "license": {
        "key": "",
        "type": license_type[data_logger]
    },
    "text": {
        "device_model": data_logger,
        "hw_details": hardware,
        "hw_version": hw_version,
        "manufacture_date": datetime.now().strftime('%Y-%m-%d'),
        "serial_number": serial_number
    }
}

eeprom_content_json = json.dumps(eeprom_content, indent=4, sort_keys=True)

try:
    with open(state_file, 'wb') as f:
        pickle.dump(eeprom_content_json, f)
    print(f"Content has been written to file: {state_file}")
except Exception as e:
    print(e)
    raise
