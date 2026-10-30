Manual Installation
-------------------
These steps mimic exactly what happens when running :code:`install.sh`, but are
simple enough they can be done manually (all you need is a text editor).

You'll need to get retropie installed on your machine before doing anything in
this guide.  Installing retropie is outside the scope of this documentation,
but an excellent method for a standalone Ubuntu machine is
`RetroPie-Setup-Ubuntu`_

The pipeline will probably work reasonably well for non-retropie setups, but
hasn't been tested and there will be some rough edges.  Those environments are
out of scope for this documentation, but if you can wrangle :code:`rph launch`
into running everything after that should work fine.

Clone the Repository
--------------------
Everything you'll need is in this project's git repository.

.. code:: bash

    $ git clone https://github.com/snewell/retropie-helpers.git

Install Userspace
-----------------
You need to install a single binary in your home directory: :code:`rph`.  It's
located within the repository's :code:`bin` folder, and you can simply create a
symlink to it from any folder currently in your :code:`PATH`.

Assuming you haven't modified :code:`PATH`, the following commands will work.

.. code:: bash

    $ mkdir bin
    $ cd bin
    $ ln -s ~/retropie-helpers/rph

Next we have to get :code:`~/bin` into your :code:`PATH`, so edit
:code:`~/.bash_profile`  You'll need to add a line like this:

.. code:: bash

    PATH="${PATH}:~/bin"

Depending on what else is in the file, you may not have :code:`rph` avaialable
in your regular shells.  If that's the case, you can add the exact same line to
:code:`~/.bashrc`.  Also be aware that some distros provide
:code:`.bash_profile` and :code:`.bashrc` stubs that exits early, so if in
doubt edit :code:`PATH` earlier in the files than later.

Lastly, you probably want the ability to change parameters to the various
:code:`rph` tools, which requires configuration files.  Everything lives in
:code:`~/.rph.d`, and you can copy the stub files from the repo as a good
starting point.

.. code:: bash

    $ cp -r ~/retropie-helpers/conf/* ~/.rph.d/


Hooking into :code:`rph` - Hijacking Retroarch
----------------------------------------------
To use :code:`rph` with :code:`retroarch`, we're going to replace the program.
This is done for a few reasons.

* :code:`retroarch` is the default emulator used for almost every system.
  Updating every :code:`emulators.cfg` file manually would be time-consuming
  and error-prone, and new systems would need to be modified as well.
* The absolute path to :code:`retroarch` is listed in every
  :code:`emulators.cfg` entry, so we can't be sneaky by prepending :code:`PATH`.
* :code:`retroarch` is relatively stable on the typical system, only being
  updated very rarely.  Even though :code:`retropie_setup.sh` will blow away
  the shim on an update, it's low effort to restore the pipeline.

Replacing the program is thankfully trivial:

.. code:: bash

    $ cd /opt/retropie/emulators/retroarch/bin
    $ sudo mv retroarch retroarch.real
    $ sudo cp ~/retropie-helpers/bin/retroarch-wrapper.sh retroarch
    $ sudo chmod 755 retroarch

This does, in order:

1. Move our working directory to the default location for :code:`retroarch`.
2. Backup the original program to :code:`retroarch.real` (the wrapper will look
   for this *exact* name)
3. Copy the wrapper in place with the name :code:`retroarch`.
4. Make sure our wrapper is executable.

At this point every emulator entry that references :code:`retroarch` will
actually be referencing the wrapper and getting injected into the :code:`rph`
pipelines.


Hooking into :code:`rph` - Standalone Emulators
-----------------------------------------------
Standalone emulators are piped by adding new entires to :code:`emulators.cfg`.
If you check system's configuration, you can see the available emulators.

.. code:: bash

    $ cat /opt/retropie/configs/gc/emulators.cfg
    dolphin = "/opt/retropie/emulators/dolphin/bin/dolphin-emu-nogui -e %ROM%"
    dolphin-gui = "/opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"
    default = "dolphin"

What you want to do is open that file in your favorite editor and add a new
entry to represent the :code:`rph` pipeline.  Copy the *entire* emulator entry
you want to base it on, give it a good name (I suggest
:code:`rph-orchestrated-<name>`) and prefix the command string with
:code:`rph launch <emulator-string>`.  For example, modifying the above we'd
get this:

.. code:: bash

    $ cat /opt/retropie/configs/gc/emulators.cfg
    dolphin = "/opt/retropie/emulators/dolphin/bin/dolphin-emu-nogui -e %ROM%"
    dolphin-gui = "/opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"
    default = "dolphin"
    rph-orchestrated-dolphin = "rph launch dolphin /opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"

Lastly, we want to set our default emulator for the system to be our new
orchestration pipeline.  The final version:

.. code:: bash

    $ cat /opt/retropie/configs/gc/emulators.cfg
    dolphin = "/opt/retropie/emulators/dolphin/bin/dolphin-emu-nogui -e %ROM%"
    dolphin-gui = "/opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"
    default = "rph-orchestrated-dolphin"
    rph-orchestrated-dolphin = "rph launch dolphin /opt/retropie/emulators/dolphin/bin/dolphin-emu -b -e %ROM%"

The valid emulator strings (this is how :code:`rph` knows what options to
support) are :code:`retroarch`, :code:`dolphin`, :code:`pcsx2`, and :code:`rpcs3`.


.. _RetroPie-Setup-Ubuntu: https://github.com/MizterB/RetroPie-Setup-Ubuntu
