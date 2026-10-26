#!/bin/bash

# Pass the true absolute binary path down to Python alongside original arguments
REAL_RA="/opt/retropie/emulators/retroarch/bin/retroarch.real"

retroarch-orchestrator.py -- "${REAL_RA}" "${@}"
