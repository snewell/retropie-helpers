#!/bin/bash

RPCS3="/opt/retropie/emulators/rpcs3-appImage/bin/rpcs3.AppImage"

MOUNT_POINT="/mnt/ps3-disc"

path=""

BUFFER_PATH="~/.cache/rpcs3/RPCS3.buf"

run() {
	${RPCS3} --no-gui "${1}/PS3_GAME/USRDIR/EBOOT.BIN"
	if [ -e ${BUFFER_PATH} ]; then
		rm ${BUFFER_PATH}
	fi
}

mount_and_run() {
	sudo mount "${1}" "${MOUNT_POINT}"
	run "${MOUNT_POINT}"
	sudo umount "${MOUNT_POINT}"
}

if [ -f "${1}" ]; then
	# we have a file, so expand it
	mount_and_run "${1}"
elif [ -d "${1}" ]; then
	# directory, so run directly
	run "${1}"
elif [ -l "${1}" ]; then
	# symbolic link, so use readlink
	real_path=$(readlink "${1}")
	if [ -f "${real_path}" ]; then
		mount_and_run "${real_path}"
	elif [ -d "${real_path}" ]; then
		run "${1}"
	fi
fi

