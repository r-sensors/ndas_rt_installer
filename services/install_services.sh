cd "$(dirname "$0")"

if [ "$1" == "enable" ]; then
    echo "Installing NDAS-RT autorun services"
    cp autorun_as_root.sh /root/ndas_rt/autorun_as_root.sh
    cp linux_ptp_master.sh /root/ndas_rt/linux_ptp_master.sh  
    cp linux_ptp_slave.sh /root/ndas_rt/linux_ptp_slave.sh  
    chmod 744 /root/ndas_rt/autorun_as_root.sh
    chmod 744 /root/ndas_rt/linux_ptp_master.sh
    chmod 744 /root/ndas_rt/linux_ptp_slave.sh
    cp ndasrt.service /etc/systemd/system/ndasrt.service   
    cp linux_ptp_master.service /etc/systemd/system/linux_ptp_master.service  
    cp linux_ptp_slave.service /etc/systemd/system/linux_ptp_slave.service  
    cp chrony.service /etc/systemd/system/chrony.service
    cp reverse_ssh.service /etc/systemd/system/reverse_ssh.service
    systemctl daemon-reload
    systemctl enable ndasrt
    systemctl start ndasrt
    systemctl enable reverse_ssh
    systemctl start reverse_ssh
    echo "Done!"
fi

if [ "$1" == "disable" ]; then 
    echo "Removing NDAS-RT from OS services"
    systemctl stop ndasrt proftpd linux_ptp_master linux_ptp_slave gpsd openvpn-client@client reverse_ssh
    systemctl disable ndasrt proftpd linux_ptp_master linux_ptp_slave gpsd openvpn-client@client reverse_ssh
    rm /etc/systemd/system/ndasrt.service
    rm /etc/systemd/system/linux_ptp_master.service
    rm /etc/systemd/system/linux_ptp_slave.service
    systemctl daemon-reload
    echo "Done!"
fi

