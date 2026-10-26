#!/bin/bash

BUFFER_PATH="~/.cache/rpcs3/RPCS3.buf"

sp3d_args=(
    "-m"
    "/mnt/ps3-disc/"
)

rpcs3_args=(
    "--no-gui"
)

setup-ps3-disc.py \
    "${sp3d_args[@]}" \
    -- \
/opt/retropie/emulators/rpcs3-appImage/bin/rpcs3.AppImage \
    "${rpcs3_args[@]}" \
    "${@}" # rom

if [ -e ${BUFFER_PATH} ]; then
    rm ${BUFFER_PATH}
fi
