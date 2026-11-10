retropie-helpers -- Tools
=========================
This folder is a collection of standalone tools that don't need to be run on a
regular basis.  They're treated as one-offs, hence why they're not part of the
:code:`rph` front door into the main toolset.

:code:`setup-tmpfs.py`
----------------------
This is a script that helps set up a :code:`tmpfs` mount.  To set up the mount,
you'll need to provide a user, group, size, and mount point.  This script with
*try* to guess values if you don't provide them, but this should be
sanity-checked.

The script will need permissions to write :code:`/etc/fstab`, which means
you'll ultimately need to run it with :code:`sudo` (e.g.,
:code:`sudo python3 setup-tmpfs.py --execute`).  The :code:`--check` flag will
also verify any current entry to see if it matches what the script will write
to :code:`/etc/fstab`.  If you provide the :code:`--execute` flag, it will
*always* do the sanity check and refuse to proceed if that fails.

Before writing to :code:`/etc/fstab`, it will make a backup of
:code:`/etc/fstab` with a timestamped filename.

.. code:: bash

    $ ls -l /etc/fstab*
    -rw-r--r-- 1 root root 1783 Nov  9 21:08 /etc/fstab
    -rw-r--r-- 1 root root 1781 Nov  9 17:31 /etc/fstab.bak
    $ sudo python3 tools/setup-tmpfs.py --execute
    Guessing tmpfs size...
        ...detected 32 GB...
        ...reserving 16 for tmpfs
    Guessing username...
        ...running as root...
        ...sudo running as pi...
    Guessing group...
        ...running as root...
        ...running with gid 1000
    Checking /etc/fstab...
        ...backing up to /etc/fstab.20261109-210930
    Verifying that mount point exists...
        ...mount point already exists
    $ ls -l /etc/fstab*
    -rw-r--r-- 1 root root 1900 Nov  9 21:09 /etc/fstab
    -rw-r--r-- 1 root root 1783 Nov  9 21:08 /etc/fstab.20261109-210930
    -rw-r--r-- 1 root root 1781 Nov  9 17:31 /etc/fstab.bak

If your system can't boot after running this script, the backup file can be
used to restore the working :code:`/etc/fstab`.
