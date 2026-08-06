import eeprom
eeprom = eeprom.EEPROM()
eeprom.read_json()

bytes_to_write = 256

print('Erasing last %u bytes...'%bytes_to_write)
data = b'\xFF'*bytes_to_write

eeprom.write(eeprom.size - bytes_to_write, data)

data = bytes(range(bytes_to_write))
print('Writing test data...')
eeprom.write(eeprom.size - bytes_to_write, data)

print('Erasing last %u bytes again...'%bytes_to_write)
data = b'\xFF'*bytes_to_write

eeprom.write(eeprom.size - bytes_to_write, data)