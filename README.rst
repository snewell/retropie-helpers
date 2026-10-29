================
retropie-helpers
================

.. image:: https://shields.io
   :target: https://github.com

A collection of lightweight, zero-dependency process wrappers designed to
transform a standard retropie_ emulation setup into a clean, automated, and
thread-safe pipeline.

What This Solves
----------------
* **Clean ROM Folders**: Forces save data into isolated per-system directories
  out of your game folders, making nightly backups effortless.
* **On-The-Fly Rom Patching**: Automatically applies standalone translation or
  hack :code:`.xdelta` patches inside isolated, zero-wear RAM memory spaces
  (:code:`tmpfs`) just before a game boots, keeping original ROM files
  untouched and ready for future patch versions.
* **Automatic Mounting of PS3 Discs**: Instead of maintaining PS3 discs as
  folders, mounts them on the fly (without root permissions) and passes the
  appropriate path to RPCS3--you can treat a PS3 dump identically to games from
  any other system.

Quick Start
-----------
To globally deploy the pipeline across **all standard system cores with zero
configuration changes**, clone this repo and run the install script.

.. code:: bash

   $ git clone https://github.com/snewell/retropie-helpers
   $ cd retropie-helpers
   $ ./install.sh

This will install :code:`rph` into user space and set up hooks into any
installed emulators we can detect in the retropie configuration.

How It Works (retroarch)
------------------------
A thin wrapper replaces :code:`retroarch` (used by most systems) and passes
control into the :code:`rph` pipeline.  That builds and executes a command
chain that applies all your settings, customizable per core, system, rom, or
anything else you want (configuration is controlled via :code:`bash`--if you
can code it, it's possible).

How it Works (Dolphin, PCSX2, RPCS3)
------------------------------------
Standalone emulators can use the same pipeline with custom entries in
:code:`emulators.cfg`.  The same wrapper trick from :code:`retroarch` would
work, but it's more hassle to maintain since standalone emulators tend to
update more frequently.

.. code:: ini

   # File location: /opt/retropie/configs/gc/emulators.cfg
   dolphin = "/opt/retropie/emulators/dolphin/bin/dolphin-emu-nogui -e %ROM%"
   dolphin-gui = "/opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"
   rph-orchestrated-dolphin = "rph launch dolphin /opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"
   default = "rph-orchestrated-dolphin"


Configuration & Upkeep
----------------------
Human-readable runtime rules are instantiated inside your home directory at
:code:`~/.rph.d/`.  Any non-default options simply require setting a handful of
variables specific to each emulator's toolchain.

Architecture & Deep Dives
-------------------------
More information is in the docs folder.  It explains how things work under the
hood in more detail for those who are curious, as well as manual installation
steps if you want to customize the install.

.. _retropie: https://retropie.org.uk

