#!/bin/bash
# ==============================================================================
# Step 1: User Space Binary & Environment Allocation
# ==============================================================================
set -euo pipefail

MY_DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))

TARGET_BIN="${HOME}/bin"
TARGET_CONF="${HOME}/.rph.d"
TARGET_SAVES="${HOME}/saves"

echo "-> Preparing local user directory workspaces..."
mkdir -p "${TARGET_BIN}" "${TARGET_CONF}" "${TARGET_SAVES}"

echo "-> Deploying user-facing entry points..."
if [ ! -e "${TARGET_BIN}/rph" ]; then
    ln -s "${MY_DIR}/../bin/rph" "${TARGET_BIN}/rph"
else
    echo "   ...rph already installed"
fi

echo "-> Deploying user-facing configuration files..."
for f in "${MY_DIR}/../conf/"*; do
    if  [ ! -f "${TARGET_CONF}/$(basename ${f})" ]; then
        echo "   ...insatlling ${f}"
        cp "${f}" "${TARGET_CONF}/"
    else
        echo "   ...skipping ${f}"
    fi
done

# Ensure binary search paths include local user utilities
PROFILE_FILE="${HOME}/.bash_profile"
[ ! -f "${PROFILE_FILE}" ] && [ -f "${HOME}/.profile" ] && PROFILE_FILE="${HOME}/.profile"

if [ ! grep -q 'HOME/bin' "${PROFILE_FILE}" 2>/dev/null ]; then
    echo -e "\n# Added by retropie-helpers bootstrap\nexport PATH=\"\$PATH:\$HOME/bin\"" >> "${PROFILE_FILE}"
    echo "✓ Added ~/bin to your path in ${PROFILE_FILE}."
else
    echo "PATH already set in ${PROFILE_FILE}"
fi
