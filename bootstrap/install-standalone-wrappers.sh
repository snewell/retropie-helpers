#!/bin/bash
# ==============================================================================
# bootstrap/patch-standalone-configs.sh
# Safely targets ONLY explicitly installed standalone emulators.
# ==============================================================================
set -euo pipefail

CONFIGS_ROOT="/opt/retropie/configs"

inject_emulator_cfg() {
    local system_name="${1}"
    local config_key="${2}"
    local launcher_script="${3}"       # Just the name: "rph launch dolphin"
    local standalone_signature="${4}"   # The signature token: "dolphin-emu"

    local cfg_file="${CONFIGS_ROOT}/${system_name}/emulators.cfg"

    # 1. Boundary Check: Exit early if the system isn't installed
    if [ ! -f "${cfg_file}" ]; then
        return 0
    fi

    # 2. Extract the matching raw line from the config file.  We want to look for a trailing space to protect against wrapper scripts.
    local raw_line
    raw_line=$(grep "${standalone_signature}[[:space:]]" "${cfg_file}" | grep -v '^rph-orchestrated' | head -n 1) || true

    # If the signature isn't found inside the file, skip gracefully
    if [ -z "${raw_line}" ]; then
        echo "   Skipping ${system_name}: Standalone signature not found."
        return 0
    fi
    echo "   Identified standalone: ${raw_line}"

    # 3. NATIVE BASH PARAMETER EXPANSION EXTRACTION:
    # Step A: Chop off everything up to the first '=' sign (isolates the quoted command)
    local quoted_command="${raw_line#*=}"

    # Step B: Strip out the leading/trailing spaces and vaporize the literal quotes
    local clean_command
    clean_command=$(echo "${quoted_command}" | tr -d '"' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

    clean_command=$(echo "${clean_command}" | sed -e 's/[[:space:]]*$//') # Clean up any trailing space

    # 4. COMPOSE THE FINAL COMMAND
    # Prepend custom launcher driver to the original stripped command string
    local final_command_string="${launcher_script} ${clean_command}"

    echo "-> Injecting optimized wrapper for standalone ${system_name}..."

    # Scrub existing key definition line to clear duplicates safely
    sed -i "/^${config_key}\s*=/d" "${cfg_file}"

    # Append our freshly constructed master command string contract
    echo "${config_key} = \"${final_command_string}\"" >> "${cfg_file}"

    # Update the default pointer to prioritize our new entry
    sed -i "/^default\s*=/d" "${cfg_file}"
    echo "default = \"${config_key}\"" >> "${cfg_file}"
}


echo "-> Scanning RetroPie configurations for standalone emulators..."

# GameCube: Only patch if standalone dolphin is present (skips if only lr-dolphin exists)
inject_emulator_cfg "gc" "rph-orchestrated-dolphin" "rph launch dolphin" "dolphin-emu"

# Wii: Only patch if standalone dolphin is present
inject_emulator_cfg "wii" "rph-orchestrated-dolphin" "rph launch dolphin" "dolphin-emu"

# PlayStation 2: Only patch if the standalone flatpak or binary is present (skips lr-pcsx2)
inject_emulator_cfg "ps2" "rph-orchestrated-pcsx2" "rph launch pcsx2" "PCSX2"

# PlayStation 3: Only patch if rpcs3 is present
inject_emulator_cfg "ps3" "rph-orchestrated-rpcs3" "rph launch rpcs3" "rpcs3"

# Restore standard user ownership over configuration artifacts
echo "✓ Standalone emulation injections finalized successfully."
