cd "$(dirname "$0")"
echo "Preparing Beaglebone for clean install"
# echo "Set new password (default ndasrt)"
# passwd debian
DEFAULT_PASSWORD="ndasrt"
TIMEOUT=10 #time to enter password
read -t $TIMEOUT -p "Enter new password (default ndasrt): " PASSWORD
if [ -z "$PASSWORD" ]; then
    PASSWORD="$DEFAULT_PASSWORD"
fi
echo "debian:$PASSWORD" | chpasswd
echo "\nNew password has been set"

systemctl disable proftpd gpsd chrony
systemctl stop proftpd gpsd gpsd.socket chrony

echo "Adjusting system clock rate"
adjtimex -f -4700000
sudo hwclock -w -f /dev/rtc0
#set valid time
ntpdate pool.ntp.org

# disable some unnecessary services
systemctl disable apache2 nginx robotcontrol.service rpcbind.service
systemctl disable bonescript-autorun.service bonescript.service bonescript.socket
systemctl disable nodered.socket nodered.service
systemctl disable unattended-upgrades.service
systemctl disable avahi-daemon.service
systemctl disable avahi-daemon.socket
systemctl stop apache2 nginx robotcontrol.service rpcbind.service
systemctl stop bonescript-autorun.service bonescript.service bonescript.socket
systemctl stop nodered.socket nodered.service
systemctl stop unattended-upgrades.service
systemctl stop avahi-daemon.service
systemctl stop avahi-daemon.socket
# remove node-red
rm -r /opt/node-red
rm /etc/avahi/services/cloud9.service
rm /etc/avahi/services/nodered.service

systemctl restart avahi-daemon
# remove introduction on cloud9 startup
#rm ../../Introduction.md
# remove unwanted directories
rm -r ../../autorun ../../BeagleBone ../../common ../../displays ../../extras ../../PocketBeagle ../../sensors
rm -rf ../../.git
# preparing installer
rm -rf ../ndas_rt/.git ../ndas_rt/.gitignore
rm -rf ../.git ../.gitmodules
rm ../README.md
# remove unwanted files
rm ../../About.md ../../Introduction.md ../../LICENSE ../../README.md ../../ToDo.md ../../.gitignore
# removing annoying popup
mv ../../.c9/plugins/beagle.bone101 ../../.c9/plugins/_beagle.bone101

# disable modswitch for Huawei modem - #ATTR{idVendor}=="12d1", ATTR{idProduct}=="15c1"
cp 40-usb_modeswitch.rules /lib/udev/rules.d/40-usb_modeswitch.rules
# change SSH banner
echo "Welcome to NDAS-RT SSH!" > /etc/issue.net
# update boot parameters to configure pins
cp uEnv.txt /boot/uEnv.txt # !!! Be extremely cautious with uname_r - should match kernel version
cp NDAS-RT-00A0.dtbo /lib/firmware/NDAS-RT-00A0.dtbo
# update cloud9 parameters to set login and password
cp standalone.js /opt/cloud9/configs/standalone.js
# update am335 driver to disable mounting getting started iso
cp bb-boot /etc/default/bb-boot
# rewrite sudoers with pmc permitions
cp sudoers /etc/sudoers
chmod 0440 /etc/sudoers

#config usb automout
cp usbmount.conf /etc/usbmount/usbmount.conf

# copy PRU firmwares
cp pru_firmwares/* /lib/firmware
# add debian to remoteproc group to access pru
usermod -a -G remoteproc debian

#install boot routines
rm -r /root/ndas_rt
mkdir /root/ndas_rt
cp boot_routines /root/ndas_rt/
chown root:root /root/ndas_rt/boot_routines
chmod 700 /root/ndas_rt/boot_routines

rm /etc/systemd/system/multi-user.target.wants/chrony.service

echo "Done!"
