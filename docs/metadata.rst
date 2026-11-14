Game Metadata
=============
:code:`rph` provides a way to access arbitrary per-game metadata.  Before
invoking the rc scripts associated with an emulator, :code:`rph` will check
for :code:`${ROM}.rphmd`.  Any key/value pairs in this file will be provided in
the variable :code:`rom_metadata`.

.. code:: bash

    $ cat ~/path/to/some/rom.rphmd
    # comments are fine
    # along with blank lines

    key = value
    # leading/trailing space is stripped
        another_key        =   some_value              # comment
    Another_key = CaseSensitive
    $ cat ~/.rph.d/retroarch.rc
    # ...
    for key in "${!rom_metadata[@]}"; do
        echo "key='${key}' value='${rom_metadata[${key}]}'"
    done
    $ rph launch retroarch --dry-run
    key='Another_key' value='CaseSensitive'
    key='key' value='value'
    key='another_key' value='some_value'
    executing ['/home/pi/retropie-helpers/libexec/rph-savepath-injector', '--root-save-dir', '/home/pi/saves', '--']

Note that :code:`rph` *does not* use this data for anything--its only role is
to read the file.

Unlike most of the configuration for :code:`rph`, an :code:`rphmd` file isn't
bash and isn't sourced by anything--they're purely key/value pairs.  Because
these live next to a rom on disk, it seemed dangerous to arbitrarily source
files in that directory.

Example Usage
-------------
I use metadata to control shared memory cards.  A simplified example for
:code:`retroarch.rc` (I use :code:`shared_save` as the shared memory card
name):

.. code:: bash

    # if enabled via metadata, let's set up shared saving
    if [ -v rom_metadata[shared_save] ]; then
        if [ ${#save_extensions[@]} -ne 0 ]; then
            sras_args+=(
                --work-dir "${GLOBAL_SCRATCH_PAD}"
                --true-save-dir "${ROOT_SAVE_PATH}/${SYSTEM}"
                --shared-base-name "${rom_metadata[shared_save]}"
                --save-extension "srm"
            )
            # we have a shared memory card, so disable the savepath-injector
            orch_args+=(
                "--savepath-injector" "disable"
            )
        else
            echo "save_extensions not defined" >&2
        fi
    fi

I have similar code for :code:`pcsx2.rc`:

.. code:: bash

    if [ -v rom_metadata[shared_save] ]; then
        umc_args+=(
            --card-name "${rom_metadata[shared_save]}"
        )
    fi

This lets me keep the details about what games need to share save data in my
roms folder (where :code:`*.rphmd` files live) and the rc files just drive the
tool arguments.  This should scale much better than matching :code:`${ROM}`
values in :code:`if` conditions.

Hypothetical Example
--------------------
I have Sinden light guns, but haven't bothered setting them up on my current
box out of pure laziness.  One of my goals is to write a tool for generic
:code:`retroarch` config injection, and then I can add a metadata tag to enable
Sinden support and inject the configuration.  Hypothetical code:

.. code:: bash

    if [ -v rom_metadata[enable_sinden] ]; then
        # inject sinden code
        rai_args+=(
            --file ~/pi/ra-configs/sinden.cfg
        )
        # future generic startup/cleanup tools
        startup_cmd+=(
            start-sinden.sh
        )
        shutdown_cmd+=(
            stop-sinden.sh
        )
    fi
