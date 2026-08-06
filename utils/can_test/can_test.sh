#!/bin/bash
ip link set can1 down
config-pin p9.24 can
config-pin p9.26 can
ip link set can1 up type can bitrate 1000000
ifconfig can1 up
