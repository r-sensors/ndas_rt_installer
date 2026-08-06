import os, select, time

'''
pin = 60
f = open('/sys/class/gpio/gpio%d/value'%pin, 'w+b')
while 1:
    f.write(b'1')
    f.seek(0)
    print(f.read())
    f.write(b'0')
    f.seek(0)
    print(f.read())

'''
#''''
pin = 65
f = open('/sys/class/gpio/gpio%d/value'%pin, 'w+b')
po = select.poll()
po.register(f, select.POLLPRI)
state_last = f.read()

while 1:
    if po.poll(1):
        #f.seek(0)
        f.read()
        print('int') 
    else: print('timeout')
    time.sleep(0.999)
    
#'''