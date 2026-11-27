import path_to_db_conn
import eeprom
import sys
import os
import db_conn


db = db_conn.DATABASE(server=("192.168.0.110", 8400), custom_key=True)
eeprom = eeprom.EEPROM()
device_data = eeprom.read_json()

request = {'cmd':'update_db', 'new_record':device_data}
response = db.request_response(request)

if 'result' not in response:
    print("Incorrect server server response")
    exit()

if response['result'] != 'OK':
    print("Server returned %s"%response['result'])
    exit()

print("Success! Server response msg: %s"%response.get("msg", ''))
