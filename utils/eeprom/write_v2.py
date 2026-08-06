import path_to_db_conn
from datetime import datetime
import json
import db_conn
import sys
import os
import re
import eeprom

eeprom = eeprom.EEPROM()

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

print("Welcome to eeprom writer!")
print("Reading old eeprom contents...")
try:
    eeprom_content_old = eeprom.read_json()
except Exception as e:
    print("Read OLD contents failed")

try:
    if eeprom_content_old["license"]["key"]:
        answer = input(
            "License key exist for this device! Do you want to rewrite eeprom? (y/n)")
        if answer != "y":
            exit()
except Exception as e:
    print(e)

data_loggers = ["NDAS-8426N", "NDAS-8446 RT"]  # dataloggers of R-Sensors
adc_boards = ["NDAS-8026 v1.4"]  # ADC of dataloggers
hws = ["NDAS-8046 v1.3", "NDAS-8044 v1.2.1",
       "NDAS-8046 v1.2"]  # hardwares of dataloggers
adc_board = adc_boards[0]  # Only one adc board is supported for NDAS-8426N
date = datetime.now().strftime('%Y-%m-%d')

data_logger = menu(data_loggers, "Choose datalogger type: ")
hardware = menu(hws, "Choose hardware version: ")

hw_version = hardware[hardware.index("v")+1:]
# serial_number = "RS005751"
while True:
    serial_number = input("Enter serial number (Example: RS005751): ")
    sn_pattern = r"^RS00\d+$"
    if re.match(sn_pattern, serial_number):
        break
    else:
        print("wrong serial number")

eeprom_content = {
    "boards": {"adc_boards": [adc_board] if data_logger == "NDAS-8426N" else [],
               "motherboard":  hardware,
               "sbc_board": "bb_green",
               **({"vcxo": "tg2016_16384"} if data_logger == "NDAS-8426N" else {})

               },
    "comment": "",
    "hw": ["Port 1"] + (["Port 2", "NDAS Port 1", "NDAS Port 2", "Slot 1"] if data_logger == "NDAS-8446 RT" else []) +
    ["5V output",
     "HTS221",
     "m41t81s",
     "MAX-M8Q",
     "NDAS_ports_Vin"],
    "license": {
        "key": "",
        "type": "ndas_rt_no_adc" if data_logger == "NDAS-8446 RT" else "ndas8426n_6ch"
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

print("Erasing...")
eeprom.erase()

print("Writing...")
eeprom.write(0, eeprom_content_json)

print("Reading new eeprom contents...")
device_data = eeprom.read_json()
print(device_data)

print("Writing eeprom content to DB")
db = db_conn.DATABASE(custom_key=True)

request = {'cmd': 'update_db', 'new_record': device_data}
response = db.request_response(request)

if 'result' not in response:
    print("Incorrect server server response")

if response['result'] != 'OK':
    print("Server returned %s" % response['result'])
else:
    print("Success! Server response msg: %s" % response.get("msg", ''))
