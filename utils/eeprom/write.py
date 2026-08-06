import eeprom
import json 
from datetime import datetime
eeprom = eeprom.EEPROM()

eeprom_data = json.dumps({
    "boards": {
        "adc_boards": [  # Для NDAS-8446 RT поле должно быть пустым
                        "NDAS-8026 v1.4"
        ],
        "motherboard": "NDAS-8044 v1.2.1",
        "sbc_board": "bb_green",
        "vcxo": "tg2016_16384"  # тип кварцевого генератора (#"cfpt126_16384")
    },
    "comment": "",  # комментарий для нас, писать ТОЛЬКО латинскими буквами
    "hw": [
        "Port 1",
        "Port 2",
        "Slot 1",  # модем/WiFi с широким разъемом
        "Slot 2",
        "NDAS Port 1",
        "NDAS Port 2",
        "5V output",
        "HTS221",  # датчик температуры/влажности (есть на ВСЕХ приборах)
        "m41t81s",  # часы реального времени (есть на ВСЕХ приборах)
        # GPS-приемник (есть на ВСЕХ приборах). На некоторых устройствах может быт MAX-M10S
        "MAX-M8Q",
        # на NDAS порты подается напряжение (есть на ВСЕХ приборах)
        "NDAS_ports_Vin",
        "PoE"  # опция "питание по Ethernet"
        'lsm303agr'  # отвечает за компас
    ],
    "license": {
        # Назначается автоматически при запуске программы 
        "key": "",
        "type": "ndas8426n_6ch"
        # ndas_rt_no_adc, ndas8426n_6ch, ndas8426n_12ch, ndas8426n_24ch
    },
    "text": {
        "device_model": "NDAS-8426N",  # "NDAS-8446 RT", "NDAS-8426N"
        "hw_details": "NDAS-8044 v1.2.1",
        "hw_version": "1.2.1",
        "manufacture_date": datetime.now().strftime('%Y-%m-%d'),
        "serial_number": "TESTTEST" # Должно быть восьмизначной строкой. Пример "RS005750"
    }
}, indent=4, sort_keys=True)
  
print("Reading old eeprom contents...")
try: eeprom.read_json()
except Exception as e: print("Read OLD contents failed")

print("Erasing...")
eeprom.erase()

print("Writing...")
eeprom.write(0, eeprom_data)

print("Reading new eeprom contents...")
eeprom.read_json()