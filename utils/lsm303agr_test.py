import time
from smbus2 import SMBus
from lib.lsm303agr import LSM303AGR

if __name__ == '__main__': 
    i2c = SMBus(2)
    lsm303 = LSM303AGR(i2c)
    try:
        while True:
            time.sleep(2)
            lsm303.read()
            print(lsm303)
            
    except KeyboardInterrupt:
        print("\nKeyboard interrupt!")
