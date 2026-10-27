================
retropie-helpers
================

.. image:: https://shields.io
   :target: https://github.com

A collection of lightweight, zero-dependency process wrappers designed to transform a standard retropie_ emulation setup into a clean, automated, and thread-safe pipeline.

What This Solves
----------------
* **Clean ROM Folders:** Forces save data and states into isolated per-system directories out of your high-value game folders, making nightly backups effortless.
* **On-The-Fly Rom Patching:** Automatically applies standalone translation or hack `.xdelta` patches inside isolated, zero-wear RAM memory spaces (`tmpfs`) right when a game boots, keeping your original ROM dump file untouched.
* **Insulated State Isolation:** Solves global file locks on emulators like PCSX2 and RPCS3, cleanly wrapping memory cards and virtual optical disc images inside unique Process-ID sub-folders that drop automatically when you exit the game.

Quick Start
-----------
Because RetroPie hardcodes absolute paths to its internal emulator binaries, this framework hooks directly in front of the engine execution sequence via a transparent binary swap. 

To globally deploy the pipeline across **all standard system cores with zero configuration changes**, run this command with root privileges:

.. code:: bash

   curl -sSL https://githubusercontent.com | sudo bash

How It Works (Invisible Interception)
-------------------------------------
The automated script safely moves RetroPie's hardcoded execution binary from ``/opt/retropie/emulators/retroarch/bin/retroarch`` to a fallback file named ``retroarch.real``. It then drops our master wrapper script into the original path location.

When a game is launched (NES, SNES, Genesis, PSX, etc.), RetroPie targets the absolute path exactly as it always does. Our wrapper intercepts the call, sets up your clean save paths and patches dynamically, and drops execution down to the true backend compiler without any performance impact or interface adjustments.

Standalone Exceptions (Dolphin, PCSX2, RPCS3)
---------------------------------------------
Non-libretro standalone emulators (such as GameCube, Wii, PS2, and PS3) bypass the global RetroArch binary directory and require an explicit launch helper entry inside their respective configuration files.

To route them, open the system's emulator config and prefix the command directly with your chosen helper script name:

.. code:: ini

   # File location: /opt/retropie/configs/ps2/emulators.cfg
   # Original Entry: flatpak run net.pcsx2.PCSX2 -fullscreen %ROM%
   
   # Hardened Composed Entry:
   unique-pcsx2 = "launch-pcsx2.sh %ROM%"
   default = "unique-pcsx2"

Configuration & Upkeep
----------------------
A human-readable runtime rules engine is instantiated inside your home workspace at ``~/.retropie-helpers.d/ra-orchestrator.rc``. 

This file is a standard, fully executable Bash shell script block. You can open it inside any text editor to drop custom edge cases, profile paths, or system exclusions on the fly without ever touching the core utility files. 

Architecture & Deep Dives
-------------------------
Please check out our detailed technical breakdown sheets inside the local ``/docs`` directory for deep explanations regarding argument array tokenization, FUSE isolation, and custom multi-user tracking layouts.

.. _retropie: https://retropie.org.uk

