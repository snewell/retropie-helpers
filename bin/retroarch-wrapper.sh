#!/bin/bash

# Pass the true absolute binary path down to Python alongside original arguments
REAL_RA="/opt/retropie/emulators/retroarch/bin/retroarch.real"

exec rph launch retroarch "${REAL_RA}" "${@}"
