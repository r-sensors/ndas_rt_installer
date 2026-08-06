import eeprom
eeprom = eeprom.EEPROM()

if __name__ == '__main__':
    eeprom.read_hex()
    eeprom.read_json()
else: 
    eeprom.read_json()
