#!/bin/bash
echo "Applying firewall rules"
/bin/bash /root/ndas_rt/firewall-rules

#echo "Mounting SD card"
#mount -o rw,users,umask=000,exec /dev/mmcblk0p1 /media/sdcard
#mount -o rw,users,exec /dev/mmcblk0p1 /media/sdcard
#chmod 777 /media/sdcard

#allow setting cpu freq from userspace
cpufreq-set -g userspace
chmod 777 /sys/devices/system/cpu/cpufreq/policy0/scaling_setspeed

echo "Changing onboard LED permitions and function"
chmod 777 /sys/class/leds/beaglebone:green:usr0/trigger
chmod 777 /sys/class/leds/beaglebone:green:usr1/trigger
chmod 777 /sys/class/leds/beaglebone:green:usr2/trigger
chmod 777 /sys/class/leds/beaglebone:green:usr3/trigger

chmod 777 /sys/class/leds/beaglebone:green:usr0/brightness
chmod 777 /sys/class/leds/beaglebone:green:usr1/brightness
chmod 777 /sys/class/leds/beaglebone:green:usr2/brightness
chmod 777 /sys/class/leds/beaglebone:green:usr3/brightness

echo "none" > /sys/class/leds/beaglebone:green:usr0/trigger
echo "none" > /sys/class/leds/beaglebone:green:usr1/trigger
echo "none" > /sys/class/leds/beaglebone:green:usr2/trigger
echo "none" > /sys/class/leds/beaglebone:green:usr3/trigger

echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness

# PINS USB LED for hw ver 0.1
#echo 60 > /sys/class/gpio/unexport
#echo 50 > /sys/class/gpio/unexport
#echo 60 > /sys/class/gpio/export #P9_12
#echo 50 > /sys/class/gpio/export #P9_14
#echo out > /sys/class/gpio/gpio115/direction
#echo out > /sys/class/gpio/gpio117/direction

echo "Setting UP GPIO_115 and GPIO_117 (AUX ADC channel selection)"
echo 115 > /sys/class/gpio/unexport
echo 117 > /sys/class/gpio/unexport
echo 115 > /sys/class/gpio/export
echo 117 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio115/direction
echo out > /sys/class/gpio/gpio117/direction

echo "Setting UP GPIO_26 and GPIO_27 (Timepulse selection)"
echo 26 > /sys/class/gpio/unexport
echo 27 > /sys/class/gpio/unexport
echo 26 > /sys/class/gpio/export
echo 27 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio26/direction
echo out > /sys/class/gpio/gpio27/direction
echo 0 > /sys/class/gpio/gpio26/value
echo 0 > /sys/class/gpio/gpio27/value

echo "Setting UP GPIO_65 (User buttons interrupt)"
echo 65 > /sys/class/gpio/unexport
echo 65 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio65/direction
echo falling > /sys/class/gpio/gpio65/edge

echo "Setting UP GPIO_49 (Reserved for future use)"
echo 49 > /sys/class/gpio/unexport
echo 49 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio49/direction
echo 0 > /sys/class/gpio/gpio49/value

echo "Setting UP GPIO_50 (ADC Timestamp)"
echo 50 > /sys/class/gpio/unexport
echo 50 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio50/direction
echo 0 > /sys/class/gpio/gpio50/value

echo "Setting UP GPIO_49 (ADC control pins)"
echo 61 > /sys/class/gpio/unexport
echo 61 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio61/direction

echo 10 > /sys/class/gpio/unexport
echo 10 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio10/direction

echo 9 > /sys/class/gpio/unexport
echo 9 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio9/direction

echo 8 > /sys/class/gpio/unexport
echo 8 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio8/direction

echo "Setting UP GPIO_81 (ADC Reset)"
echo 81 > /sys/class/gpio/unexport
echo 81 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio81/direction

echo "Setting UP GPIO_80 (ADC Sync)"
echo 80 > /sys/class/gpio/unexport
echo 80 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio80/direction

echo 61 > /sys/class/gpio/unexport
echo 61 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio61/direction
echo 0 > /sys/class/gpio/gpio61/value

echo "Starting gpsd"
gpsd -n -b /dev/ttyS4
#gpsd -n -N -D 1 /dev/ttyS4

echo 'Executing boot routines'
/root/ndas_rt/boot_routines --host "192.168.0.110"

echo "Starting NDAS-RT system manager"
sudo -u debian python3 /var/lib/cloud9/ndas_rt/ndas_rt.py
