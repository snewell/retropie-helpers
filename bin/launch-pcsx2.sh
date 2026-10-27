#!/bin/bash

LOCK_FILE="/dev/shm/pcsx2_global_memcard.lock"

umc_args=(
    "--save-dir"
    "/home/pi/saves/ps2"
)

pcsx2_args=(
    "-fullscreen"
)

# The order matters here: we need to make the unique memory card first, since
# that depends on the actual path of the rom.  We could be passing a different
# rom to pcsx2 after xdelta-patcher, but the memory card symlink is already set
# up to the right place.
#
# We're goig to prefix everything with flock since PCSX2 treats memory cards as
# global.
flock -x -w 3 "${LOCK_FILE}" \
unique-memcard.py \
    "${umc_args[@]}" \
    -- \
xdelta-patcher.py -- \
flatpak run net.pcsx2.PCSX2 \
    "${pcsx2_args[@]}" \
    "${@}" # rom
