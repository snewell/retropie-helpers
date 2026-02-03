#!/bin/bash

set -e

SCRATCH="/mnt/scratch"

last="${@: -1}"
out_file="${last}"
filename=$(basename "${last}")
full_filename="${last%.*}"
xdelta_file="${full_filename}.xdelta"
if [ -e "${xdelta_file}" ]; then
	out_file="${SCRATCH}/${filename}"
	xdelta3 -d -s "${last}" "${xdelta_file}" "${out_file}"
fi

# execute
${@:1:$#-1} "${out_file}"

# cleanup
if [[ "${out_file}" == "${SCRATCH}"* ]]; then
	rm "${out_file}"
fi

