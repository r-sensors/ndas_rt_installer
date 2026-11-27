import path_to_db_conn
from datetime import datetime
import db_conn
import eeprom
import pickle
import os, sys

state_file = "/tmp/eeprom.pkl"

eeprom = eeprom.EEPROM()

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
            sys.exit()
except Exception as e:
    print(e)

if os.path.exists(state_file):
    with open(state_file, "rb") as f:
        eeprom_content_json = pickle.load(f)
else:
    print("There is no eeprom content! Create eeprom content first.")
    sys.exit()

print(eeprom_content_json)
print("Erasing...")
eeprom.erase()

print("Writing...")
eeprom.write(0, eeprom_content_json)

print("Reading new eeprom contents...")
device_data = eeprom.read_json()
print(device_data)

print("Writing eeprom content to DB")
db = db_conn.DATABASE(server=("192.168.0.110", 8400), custom_key=True)

request = {'cmd': 'update_db', 'new_record': device_data}
response = db.request_response(request)

if 'result' not in response:
    print("Incorrect server server response")

if response['result'] != 'OK':
    print("Server returned %s" % response['result'])
else:
    print("Success! Server response msg: %s" % response.get("msg", ''))
