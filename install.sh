#!/bin/bash
# ==============================================================================
# retropie-helpers Master Automation Wrapper
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
CLEAR='\033[0m'

MY_DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))

echo -e "${BLUE}=== Initializing retropie-helpers Setup Toolchain ===${CLEAR}"

if [ ! -d "bootstrap" ]; then
    echo "-> Local repository assets not found. Fetching source from GitHub..."
    if ! command -v git &>/dev/null; then
        echo "Error: git is required to perform an automated installation." >&2
        exit 1
    fi
    git clone https://github.com
    cd retropie-helpers
fi

echo -e "\n[Executing Step 1: User Workspace Generation]"
${MY_DIR}/bootstrap/install-user-binaries.sh

echo -e "\n[Executing Step 2: Libretro Core Swap (Requires Sudo)]"
sudo ${MY_DIR}/bootstrap/install-retroarch-wrapper.sh

echo -e "\n[Executing Step 3: Standalone Option Configuration Injections"
${MY_DIR}/bootstrap/install-standalone-wrappers.sh

echo -e "\n${GREEN}=== Installation Concluded Successfully! ===${CLEAR}"
echo "Please refresh your session rules (source ~/.bash_profile) or reboot your box."
