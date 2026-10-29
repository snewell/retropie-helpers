#!/bin/bash
# ==============================================================================
# Step 2: Global Libretro Hardcoded Path Interception
# ==============================================================================
set -euo pipefail

MY_DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo "~${REAL_USER}")
RA_BIN_DIR="/opt/retropie/emulators/retroarch/bin"

if [ ! -d "${RA_BIN_DIR}" ]; then
    echo "Error: Standard RetroArch directory tree not found at ${RA_BIN_DIR}." >&2
    exit 1
fi

echo "-> Performing secure binary swap within ${RA_BIN_DIR}..."
if [ -f "${RA_BIN_DIR}/retroarch" ] && [ ! -f "${RA_BIN_DIR}/retroarch.real" ]; then
    echo "   Backing up raw executable to retroarch.real..."
    mv "${RA_BIN_DIR}/retroarch" "${RA_BIN_DIR}/retroarch.real"
fi

# make sure if retroarch still exists, it's our wrapper script
if [ -e "${RA_BIN_DIR}/retroarch" ]; then
    mt=$(file --mime-type -b "${RA_BIN_DIR}/retroarch")
    if [ "${mt}" != "text/x-shellscript" ]; then
        echo "Unxpected filetype of retroarch (${mt})" >&2
        exit 1
    fi
fi
echo "   Deploying master path wrapper script into position..."
cp "${MY_DIR}/../bin/retroarch-wrapper.sh" "${RA_BIN_DIR}/retroarch"
chmod +x "${RA_BIN_DIR}/retroarch"
echo "✓ Global core hijacking setup successfully finalized."
