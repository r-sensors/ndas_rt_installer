import smbus2
import os, time, ctypes, struct
from os import path

# Get I2C bus
bus = smbus2.SMBus(2)
clib = ctypes.CDLL(path.join(path.abspath(path.dirname(__file__)), 'lib/hts221.so'))

bus.write_byte_data(0x5F, 0x10, 0x3F)
bus.write_byte_data(0x5F, 0x20, 0x81)
eeprom = bytes(bus.read_i2c_block_data(0x5F, 0x30|0x80, 16))
eeprom_struct = struct.unpack('<6B5H', eeprom)
T0_val_x8 = eeprom_struct[2] 
T1_val_x8 = eeprom_struct[3] 
T0_msb = (eeprom_struct[5] &0x03) * 256
T1_msb = (int(eeprom_struct[5] / 4) &0x03) * 256
Hx0 = eeprom_struct[6] 
Hx1 = eeprom_struct[8] 
Hy0 = eeprom_struct[0] * 5
Hy1 = eeprom_struct[1] * 5
Tx0 = eeprom_struct[9]
Tx1 = eeprom_struct[10]
Ty0 = (T0_val_x8 + T0_msb)*5/4
Ty1 = (T1_val_x8 + T1_msb)*5/4
Tk = (Ty1 - Ty0)*65536/(Tx1 - Tx0)
Tb = Ty0 - ((Tx0 * Tk)/65536)
Hk = (Hy1 - Hy0)*65536/(Hx1 - Hx0)
Hb = Hy0 - ((Hx0 * Hk)/65536)
coeffs = b'\0'*8
retval = clib.hts221_init(eeprom, coeffs)
if retval == 0: print('SUCCESS')
print(coeffs)
print('%d %d %d %d' %(Tk, Tb, Hk, Hb))
time.sleep(1)

while(1):
    os.system('clear')
    result = b'\0'*4
    data = bytes(bus.read_i2c_block_data(0x5F, 0x26 | 0x80, 6))
    retval = clib.hts221_data_get(data, coeffs, result)
    print(retval)
    print(result)
    
    humidity, cTemp = struct.unpack('hh', result)
    
    # Output data to screen
    
    print("Humidity: %f" %humidity)
    print("Temperature: %f" %cTemp)
    
    time.sleep(1)