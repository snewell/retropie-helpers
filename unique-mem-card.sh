#!/bin/bash

memcard_exists() {
	if [ -f "${1}" ]; then
		# see if it's a symlink
		if [ -L "${1}" ]; then
			# it's a symlink, so okay
			return 1
		fi
		echo "Memcard already exists (${1})" >&1
		return 0
	fi
	return 1
}

make_mc_symlink() {
	base_name="${1}"
	mc_name="${2}"
	suffix="${3}"

	ln -sf "${base_name}.srm${suffix}" "${mc_name}"
}

shared_memcard8="Mcd001.ps2"
shared_memcard32="Shared Memory Card (32 MB).ps2"

rom_name="${@: -1}"
rom_dir_name=$(dirname "${rom_name}")

slot1_dir="${rom_dir_name}/Slot 1"

full_shared_memcard8_path="${slot1_dir}/${shared_memcard8}"
full_shared_memcard32_path="${slot1_dir}/${shared_memcard32}"

memcards=("${full_shared_memcard8_path}" "${full_shared_memcard32_path}")
for mc in "${memcards[@]}"; do
	if memcard_exists "${mc}"; then
		exit 1
	fi
done

# we can make the cards
# rom_without_extension=$(echo ${rom_name} | sed 's/\..*$//')
rom_without_extension=${rom_name%.*}
if ! make_mc_symlink "${rom_without_extension}" "${full_shared_memcard8_path}" "8"; then
	echo "Error setting up memory card ${full_shared_memcard8_path}"
	exit 1
fi
if ! make_mc_symlink "${rom_without_extension}" "${full_shared_memcard32_path}" "32"; then
	echo "Error setting up memory card ${full_shared_memcard32_path}"
	exit 1
fi

# start the game
flatpak run net.pcsx2.PCSX2 -fullscreen "${rom_name}"
# try to clean up symlinks
rm "${full_shared_memcard8_path}"
rm "${full_shared_memcard32_path}"

