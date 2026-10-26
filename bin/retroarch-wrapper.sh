#!/bin/bash

RC_FILE=~/".retropie-helpers.d/ra-orchestrator.rc"
INFO_FILE=/dev/shm/runcommand.info

# Pass the true absolute binary path down to Python alongside original arguments
REAL_RA="/opt/retropie/emulators/retroarch/bin/retroarch.real"

spi_args=()
xdp_args=()
orch_args=()

if [ -e "${INFO_FILE}" ]; then
    SYSTEM=$(sed '1q;d' "${INFO_FILE}")
    CORE=$(sed '2q;d' "${INFO_FILE}")
    ROM=$(sed '3q;d' "${INFO_FILE}")
fi

# Fallback constants to prevent unbound variable crashes inside rc logic
# TODO: guess these from arguments
SYSTEM="${SYSTEM:-unknown}"
CORE="${CORE:-unknown}"
ROM="${ROM:-unknown}"

if [ -e ${RC_FILE} ]; then
    . ${RC_FILE}
fi

# Matrix Map: "Local Array Name" : "Target Orchestrator Flag"
declare -A tool_map
tool_map[spi_args]="--savepath-injector-arg"
tool_map[xdp_args]="--xdelta-patcher-arg"

orch_payload=("${orch_args[@]}")
# Dynamically parse and expand any populated arrays
for array_name in "${!tool_map[@]}"; do
    target_flag="${tool_map[${array_name}]}"

    # Use Bash Variable Indirection to safely extract values from the array name string
    indirect_reference="${array_name}[@]"
    array_values=("${!indirect_reference}")

    if [ ${#array_values[@]} -gt 0 ]; then
        for item in "${array_values[@]}"; do
            orch_payload+=("${target_flag}=${item}")
        done
    fi
done


echo -e "executing" retroarch-orchestrator.py "${orch_payload[@]}" -- "${REAL_RA}" "${@}" "\n\n"
retroarch-orchestrator.py "${orch_payload[@]}" -- "${REAL_RA}" "${@}"
