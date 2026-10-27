#!/bin/bash
# ==============================================================================
# retropie-helpers Automated Master Installer
# - Perfroms Deep Interception for standard Libretro Cores
# - Automatically injects standalone launcher contracts into emulators.cfg
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CLEAR='\033[0m'

echo -e "${BLUE}=== Starting retropie-helpers Deep Installation ===${CLEAR}"

# Enforce root execution since we are modifying global configurations
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This binary swap installer must be run with sudo privileges.${CLEAR}" >&2
    echo "Usage: sudo ./install.sh" >&2
    exit 1
fi

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo "~${REAL_USER}")

TARGET_BIN="${REAL_HOME}/bin"
TARGET_CONF="${REAL_HOME}/.retropie-helpers.d"
TARGET_SAVES="${REAL_HOME}/saves"
RA_BIN_DIR="/opt/retropie/emulators/retroarch/bin"
CONFIGS_ROOT="/opt/retropie/configs"

echo "-> Preparing user workspace directory allocations..."
mkdir -p "${TARGET_BIN}"
mkdir -p "${TARGET_CONF}"
mkdir -p "${TARGET_SAVES}"

# 1. Populate the local driver binaries
echo "-> Synchronizing executable scripts to ${TARGET_BIN}..."
if [ -d "bin" ]; then
    cp bin/* "${TARGET_BIN}/"
    chmod +x "${TARGET_BIN}"/*.sh "${TARGET_BIN}"/*.py
    chown -R "${REAL_USER}:${REAL_USER}" "${TARGET_BIN}"
fi

if [ -f "conf/ra-orchestrator.rc" ] && [ ! -f "${TARGET_CONF}/ra-orchestrator.rc" ]; then
    echo "-> Instantiating profile rules template to ${TARGET_CONF}..."
    cp conf/ra-orchestrator.rc "${TARGET_CONF}/"
    chown -R "${REAL_USER}:${REAL_USER}" "${TARGET_CONF}"
fi

# 2. PERFORM THE DEEP BINARY HIJACK (Libretro Core Interception)
echo -e "-> Evaluating RetroArch absolute installation paths inside ${RA_BIN_DIR}..."
if [ -d "${RA_BIN_DIR}" ]; then
    if [ -f "${RA_BIN_DIR}/retroarch" ] && [ ! -f "${RA_BIN_DIR}/retroarch.real" ]; then
        echo -e "-> ${GREEN}Backing up original RetroArch binary to retroarch.real...${CLEAR}"
        mv "${RA_BIN_DIR}/retroarch" "${RA_BIN_DIR}/retroarch.real"
    fi
    echo -e "-> ${GREEN}Deploying transparent interception wrapper to retroarch target...${CLEAR}"
    cp "${TARGET_BIN}/retroarch-wrapper.sh" "${RA_BIN_DIR}/retroarch"
    chmod +x "${RA_BIN_DIR}/retroarch"
    ln -sf "${RA_BIN_DIR}/retroarch" "${TARGET_BIN}/retroarch"
else
    echo -e "${YELLOW}Warning: Hardcoded RetroArch installation folder not found at ${RA_BIN_DIR}. Skipping core hijack.${CLEAR}"
fi

# 3. AUTOMATED EMULATORS.CFG STANDALONE PLUMBING ENGINE
# Helper function to inject entries safely into RetroPie's config files without duplicates
inject_emulator_cfg() {
    local system_name="$1"
    local config_key="$2"
    local command_string="$3"
    local cfg_file="${CONFIGS_ROOT}/${system_name}/emulators.cfg"

    # Enforce parent directory presence if they haven't launched the system yet
    mkdir -p "$(dirname "${cfg_file}")"
    touch "${cfg_file}"

    echo -e "   Configuring ${BLUE}${system_name}${CLEAR} -> ${GREEN}${config_key}${CLEAR}..."

    # Scrub any existing key definition line to clear path collisions cleanly
    sed -i "/^${config_key}\s*=/d" "${cfg_file}"

    # Append the fresh master definition string contract
    echo "${config_key} = \"${command_string}\"" >> "${cfg_file}"

    # Intelligently set the helper wrapper as the system default option
    sed -i "/^default\s*=/d" "${cfg_file}"
    echo "default = \"${config_key}\"" >> "${cfg_file}"
}

echo "-> Injecting specialized standalone driver wrappers..."

# GameCube Configuration Injection
inject_emulator_cfg "gc" "unique-dolphin" "launch-dolphin.sh %ROM%"

# Wii Configuration Injection
inject_emulator_cfg "wii" "unique-dolphin" "launch-dolphin.sh %ROM%"

# PlayStation 2 Configuration Injection
inject_emulator_cfg "ps2" "unique-pcsx2" "launch-pcsx2.sh %ROM%"

# PlayStation 3 Configuration Injection
inject_emulator_cfg "ps3" "unique-rpcs3" "launch-rpcs3.sh %ROM%"


# 4. Synchronize user environmental search paths for convenience tools
PROFILE_FILE="${REAL_HOME}/.bash_profile"
if [ ! -f "${PROFILE_FILE}" ] && [ -f "${REAL_HOME}/.profile" ]; then
    PROFILE_FILE="${REAL_HOME}/.profile"
fi

if ! grep -q 'HOME/bin' "${PROFILE_FILE}" 2>/dev/shm/null; then
    echo "" >> "${PROFILE_FILE}"
    echo 'export PATH="$PATH:$HOME/bin"' >> "${PROFILE_FILE}"
    chown "${REAL_USER}:${REAL_USER}" "${PROFILE_FILE}"
fi

# Fix ownership across configuration artifacts to prevent lock errors
chown -R "${REAL_USER}:${REAL_USER}" "${CONFIGS_ROOT}"

echo -e "\n${GREEN}=== Global Deep Interception & Configuration Completed! ===${CLEAR}"
echo "All Libretro and standalone wrapper systems are successfully integrated."

