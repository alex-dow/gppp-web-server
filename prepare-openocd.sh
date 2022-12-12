#!/bin/bash
###############################################################################
# General Purpose Precision Pointer Project                                   #
###############################################################################
# This script builds and compiles an RP2040-combpatible version of OpenOCD    #
#                                                                             #
# It is setup to compile on a raspberry pi                                    #
###############################################################################
set -e
cd ~
[ ! -d "openocd" ] && mkdir openocd
git clone https://github.com/raspberrypi/openocd.git --branch picoprobe --depth=1 --no-single-branch openocd-git
cd openocd-git
./bootstrap
./configure --enable-sysfsgpio --enable-bcm2835gpio --prefix=/home/pi/openocd
make
make install
