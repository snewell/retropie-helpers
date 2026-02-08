retropie-helpers
================
This repository is a collection of wrapper scripts I use to supplement/modify a
standard retropie_ installation.  I've maintained these in piecemeal for a few
years, and figured it's easier to put them in a repo so that it's easier to drop
them in future systems, plus pass them on as needed.

These have been tested only on my setup, which looks mostly like this:

* A clean Ubuntu 24.04 Server install
* Install `RetroPie-Setup-Ubuntu`_
* Manually adding emulator entries to the various emulator configs

Available Scripts
-----------------
:code:`dolpin-wrapper.sh`
  Forces a different version of systemd to be pre-loaded.  This gets around a bug
  in the systemd version installed in Ubuntu 24.04 (TODO: find the bug again and
  link to it) that caused dolphin to sometimes crash.  Since I didn't want to mess
  with the system-wide version of systemd, this lets me get around the bug.

  First attempt was to disable systemd support in dolphin, but that never seemed
  to work.

  You'll need to manually get a copy of a working systemd, but it's easy to
  download/build yourself.  The wrapper directory is hardcoded in this scipt.

:code:`ps3-wrapper.sh`
  PS3 games are folders, which I find untidy.  This mounts a disc to a temporary
  directory and passes the appropriate path the emulator.  There are obvious
  checks to see if it's working with a directory or a symlink.

:code:`unique-mem-card.sh`
  I prefer unique save data per game, but PCSX2 uses shared memory cards.  This
  just sets up symlinks to make this happen.

  If I want to share a memory card, I'll create the appropriate symlinks directly.

:code:`xdelta-patcher.py`
  Not all emulators support soft patching, so this is a wrapper to step in where
  it's not supported directly.  As emulators/core add support for soft patching,
  this should be less useful.

  This essentially requires a tmpfs.  Something like this in :code:`/etc/fstab`
  will do the trick:

  .. code::

    tmpfs   /mnt/scratch   tmpfs   size=10G,uid=pi,gid=pi,mode=755,noatime 0 0


Using the Scripts
-----------------
For the most part, you'll want to add a new emulator to a system's emulator
config.  All the scripts will pass trailing arguments on, but when they need to
operate on a rom they assume it's the last argument (true for everything at the
time I'm writing this).  This means your emulator config should look something
like this:

.. code:: bash

  $ cat /opt/retropie/configs/psp/emulators.cfg
  lr-ppsspp = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-ppsspp/ppsspp_libretro.so --config /opt/retropie/configs/psp/retroarch.cfg %ROM%"
  xdelta-lr-ppsspp = "xdelta-patcher.py -- /opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-ppsspp/ppsspp_libretro.so --config /opt/retropie/configs/psp/retroarch.cfg %ROM%"
  default = "xdelta-lr-ppsspp"

Copy and paste whatever entry you like, then just prefix it with the relevant
script.

Make sure these scripts are in :code:`PATH`.  The easiest way is to edit your
:code:`.bash_profile` and restart.

.. code:: bash

  $ head .bash_profile
  PATH="${PATH}:/home/pi/bin"
  # other stuff that was already there

If you want to run these scripts in an interactive shell, add them to your
:code:`.bashrc` as well.

:code:`unique-mem-card.sh` and :code:`dolphin-wrapper.sh` will call
:code:`xdelta-patcher.py`.

I'll add more detailed documentation to the scripts at some point.

.. _retropie: https://retropie.org.uk
.. _RetroPie-Setup-Ubuntu: https://github.com/MizterB/RetroPie-Setup-Ubuntu
