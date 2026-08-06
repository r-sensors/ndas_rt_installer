#!/bin/bash
echo "Starting LinuxPTP as slave only"
ptp4l -i eth0 -H -s &
phc2sys -a -r
