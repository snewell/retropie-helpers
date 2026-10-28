Command Pipeline
================
A central design principle is that scripts are turned into pipelines in a way
that's very similar to the way Unix pipes work on the command line.  At a high
level, each piece of a chain looks like this:

.. code:: bash

    <script> [script arguments] -- <next script> [arguments]

The final piece is ultimately the emulator, but the environment has been
prepared by each piece before it in the chain.  As a practical example, let's
break down :code:`launch-pcsx2`.

To play a PS2 game, we need to do a few things:

* setup unique memory cards
* apply available patches
* launch the game

Instead of writing one script that does everything, each of those steps is a
separate script that does just that job.  It makes each script easier to test
and enhance, since it's trivial to verify the output is the same.

The pipeline looks like this:

.. code:: bash

    flock -x -w 3 "${LOCK_FILE}" \
    unique-memcard.py \
        "--save-dir" \
        "/home/pi/saves/ps2" \
        -- \
    xdelta-patcher.py -- \
    flatpak run net.pcsx2.PCSX2 \
        "-fullscreen" \
        "${@}" # rom

:code:`flock` makes sure we don't run more than one instance of PCSX2 at a time
(it uses global memory cards, and the rest of the pipeline would break).

:code:`unique-memcard` sets up symlinks to convert the global memory cards that
PCSX2 uses into game-specific memory cards.  The actual emulator still thinks
it's using global memory cards and writes to those files, but they're just
symbolic links to the location we actually want the save data to live.

:code:`xdelta-patcher` will check for--and apply--available xdelta patches for
our games.  It will also recursively patch the contents of cue and m3u files if
necessary, and update any future arguments (the rom) to reference the location
of the patched file instead of the original path.

Finally, with everything ready to go, we can launch the emulator and play our
game.

Once the emulator exits, each script can run its independent cleanup work.
:code:`xdelta-patcher` cleans up the patched files it creates,
:code:`unique-memcard` removes the temporary symlinks, and :code:`flock` removes
its file lock.  If necessary, we could apply everything before the emulator
itself into other command chains.
