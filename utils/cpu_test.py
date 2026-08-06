import time

while True:
    a = 10000000
    while a > 0:
        a -= 1
    time.sleep(1)
    print("Cycle")