import struct
import os, time

path = '/sys/bus/iio/devices/iio:device0/in_voltage'

def get_main_ch_value(f):
    voltage = 0
    dummy = f.read()
    for i in range(50): 
        f.seek(0)
        voltage += int(f.read())
    return round(((voltage)/4096/50) * 1.8,2)
    
l = [open(path+str(i+1)+'_raw', 'r') for i in range(7)]

while True:
  #  v = [get_main_ch_value(f) for f in l]

  #  os.system('clear')
  #  print(v)

    time.sleep(1)
