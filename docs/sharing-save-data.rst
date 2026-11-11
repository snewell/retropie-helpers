Sharing Save Data
=================
Sharing save data is slightly trickier than it first seems since :code:`rph`
wants to protect against emulators performing atomic writes.  The naive
solution of symlinking save files (which I used for several years) falls apart
in the following scenario:

1. The emulator writes the save to a temporary file
2. The emulator deletes the original file (a symlink)
3. The emulator moves the new save into place

To fix this, :code:`rph` performs the following steps if you want to share save
files:

1. (if it exists) Copy the shared save into the path the emulator expects.
2. Let the emulator handle saving however it chooses, including the atomic
   write pattern described above
3. After the emulator exits, copy the temporary save file back to the shared
   location

Working with :code:`retroarch` Cores
------------------------------------
There's an extra tool in the :code:`retroarch` pipeline to handle this, and it
can be driven entirely through :code:`~/.rph.d/retroarch.rc`.  A simplified
example might look like this:

.. code:: bash

    if [[ "${ROM}" == *"Suikoden"* ]]; then
        sras_args+=(
            --work-dir "${GLOBAL_SCRATCH_PAD}" # temporary save/config files
            --true-save-dir "${ROOT_SAVE_PATH}/${SYSTEM}" # where the real save file lives
            # the next two lines will evaluate to "Suikoden.srm"
            --shared-base-name "Suikoden"
            --save-extension "srm"
            # --save-extension can be repeated if there are multiple save files to copy
        )
        # we have a shared memory card, so disable the savepath-injector
        orch_args+=(
            "--savepath-injector" "disable"
        )
    fi

Working with :code:`PCSSX2`
---------------------------
This is actually much easier than :code:`retroarch` since there's a fixed
memory card folder.  Put a snippet like the following into
:code:`~/.rph.d/pcsx2.rc`.

.. code:: bash

    # other umc_args settings
    # ...
    if [[ "${ROM}" == *"Suikoden"* ]]; then
        umc_args+=(
            --card-name "Suikoden"
        )
    fi
