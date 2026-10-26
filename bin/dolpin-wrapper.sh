#!/bin/bash

# export LD_LIBRARY_PATH=/home/pi/systemd/systemd-257.5/build
export LD_LIBRARY_PATH=/home/pi/systemd/systemd-260.1/build
exec "${@}"
