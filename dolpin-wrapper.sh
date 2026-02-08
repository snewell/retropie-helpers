#!/bin/bash

export LD_LIBRARY_PATH=/home/pi/systemd/systemd-257.5/build
exec xdelta-patcher.py "${@}"
