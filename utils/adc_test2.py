import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import struct
import os, time

ADC.setup()
GPIO.setup("P9_27", GPIO.OUT)
GPIO.setup("P9_25", GPIO.OUT)
GPIO.output("P9_25", GPIO.LOW)
GPIO.output("P9_27", GPIO.LOW)

ct = 0

def get_aux_ch_value(chnum):
    if chnum == 0:
        GPIO.output("P9_25", GPIO.LOW)
        GPIO.output("P9_27", GPIO.LOW)
    elif chnum == 1:
       GPIO.output("P9_25", GPIO.HIGH)
       GPIO.output("P9_27", GPIO.LOW)
    elif chnum == 2:
        GPIO.output("P9_25", GPIO.LOW)
        GPIO.output("P9_27", GPIO.HIGH)
    elif chnum == 3:
       GPIO.output("P9_25", GPIO.HIGH)
       GPIO.output("P9_27", GPIO.HIGH)
    time.sleep(0.005)
    t0 = time.time()
    voltage = 0
    dummy = ADC.read("AIN0")
    for i in range(20): voltage += ADC.read("AIN0")
    return round(voltage*3/20,2)
    
def get_main_ch_value(chnum):
    voltage = 0
    chname = "AIN"+str(chnum)
    dummy = ADC.read(chname)
    for i in range(50): voltage += ADC.read(chname)
    return round(voltage/50*1.8,2)

while True:
    v0 = get_aux_ch_value(0) 
    v1 = get_aux_ch_value(1)
    v2 = get_aux_ch_value(2) 
    v3 = get_aux_ch_value(3)
    v11 = get_main_ch_value(1)
    v12 = get_main_ch_value(2)
    v13 = get_main_ch_value(3)
    v14 = get_main_ch_value(4)
    v15 = get_main_ch_value(5)
    v16 = get_main_ch_value(6)
    v17 = get_main_ch_value(7)
    
    os.system('clear')
  #  print(ct)
  
    print('aux1: '+ str(v0) + 'V', end = '\t')
    print('aux2: '+ str(v1) + 'V', end = '\t')
    print('aux3: '+ str(v2) + 'V', end = '\t')
    print('aux4: '+ str(v3) + 'V', end = '\n')

    print('ch1: '+ str(v11) + 'V', end = '\t')
    print('ch2: '+ str(v12) + 'V', end = '\t')
    print('ch3: '+ str(v13) + 'V', end = '\t')
    print('ch4: '+ str(v14) + 'V', end = '\t')
    print('ch5: '+ str(v15) + 'V', end = '\t')
    print('ch6: '+ str(v16) + 'V', end = '\n')
    print('ch7: '+ str(v17) + 'V [!!ALLWAYS CONNECTED TO Vdd!!]')
    print('')
    print('Main in current: ' + str(v0*v2) + ' W')
    print('RS_485_2_Curr: ' +str(v1*v2) + ' W')
    print('Main in voltage: ' + str(v2/0.05) +' V')
    print('RS_485_1_Curr: ' +str(v3*v2) + ' W')
    
 #   GPIO.output("P9_25", GPIO.HIGH)
 #   GPIO.output("P9_27", GPIO.LOW)
 #   time.sleep(0.01)
 #   voltage = ADC.read("AIN0")
 #   print("10:", voltage)

    time.sleep(1)

#while counter < n_of_samples:
#    voltage = ADC.read("AIN1")
 #   voltage = value * 1.8
#    f.write(bytearray(struct.pack("f", voltage)))
#    counter += 1
#    if counter % 3000 == 0: 
#        if gpio_state == GPIO.HIGH: gpio_state = GPIO.LOW
#        else: gpio_state = GPIO.HIGH
#        GPIO.output("P9_27", gpio_state)
#       el = round(time.time() - start_time, 2)
#        print("C=", counter/1000, " V=",round(voltage, 4), " EL=", el, "s")
        