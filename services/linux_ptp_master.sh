#!/bin/bash
echo "Starting LinuxPTP as master"
ptp4l -i eth0 -H &
phc2sys -a -rr
