#!/bin/bash

dolphin_args=(
)

DOLPHIN_EXE="/opt/retropie/emulators/dolphin/bin/dolphin-emu"

# Not sure if dolphin-wrapper has to be first, but I haven't tested any other
# way.  Probably doesn't hurt to pre-load the systemd libraries though, and I'm
# too lazy to test otherwise.
dolpin-wrapper.sh \
xdelta-patcher.py -- \
${DOLPHIN_EXE} \
    "${dolphin_args[@]}" \
    -e "${@}" # -e is required before passing the last rom file
