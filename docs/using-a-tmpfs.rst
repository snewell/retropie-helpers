Using a :code:`tmpfs` file system
=================================
:code:`rph` tools heavily depend on creating scratch files, and this will be
much faster if you have a :code:`tmpfs` mount available.  It provides the
following advantages:

* No wear on your physical storage.  Because the file system lives entirely in
  ram, your physical storage suffers no write cycles.
* Much faster performance in most cases.  Ram is almost always faster to read
  and write than persistent storage, so the scripts finish faster and launch
  your games sooner.
* Automatic cleanup on system boot.  Because the file system lives in ram, once
  your system is powered down everything on it ceases to exist.  This makes it
  perfect for temporary work, since even if files aren't cleaned up due to a
  bug or crash in the :code:`rph` code, nothing clutters your system over time.
* Passive ram use.  Even if you allocate a large amount of space, it takes only
  minimal ram to maintain the mount point.  As :code:`rph` cleans up its
  temporary files, your ram will be restored to whatever needs it on your
  system.

Setting it up
-------------
The easiest method is to use :code:`setup-tmpfs.py` under the :code:`tools`
folder.  If you want to set it up manually though, you'll need to edit
:code:`/etc/fstab`.  That's the file that controls all the file systems your
system mounts at boot.

**Before you begin**: make sure to backup the current version of
:code:`/etc/fstab`.  If you fat-finger the file, the backup can be restored to
keep your system booting.

The file is plain text, so open it with your favorite text editor (:code:`nano`
is easy to use).  You'll want to add a new line that looks something like this:

.. code::

    tmpfs   /mnt/scratch    tmpfs   size=16G,uid=pi,gid=pi,mode=755,noatime 0 0

Here's what each column does:

**:code:`tmpfs`** (column 1)
    The device to mount.  Because we're doing :code:`tmpfs`, we don't have a
    physical device.

**:code:`/mnt/scratch`** (column 2)
    The location on disk where our :code:`tmpfs` will be exposed.  This folder
    will have to exist before the :code:`tmpfs` can be mounted, so make sure
    you create the directory if it doesn't exist (e.g.,
    :code:`sudo mkdir -p /mnt/scratch`).

    This is the folder you'll pass as the work/scratch directory to all the
    :code:`rph` tools.

**:code:`tmpfs`** (column 3)
    The file system the device uses.  This is again :code:`tmpfs`.

**Mount Options** (column 4)
    A comma-separated list of extra options to apply when the :code:`tmpfs` is
    mounted.  The ones here:

    :code:`size=16G`
        Set the maximum size to 16 GB.  This value is *highly* dependent on
        your system and use case.

    :code:`uid=pi`
        Sets user ownership of the mount to the :code:`pi` user.  This username
        should match whatever Linux user is going to actually be running
        :code:`rph`.

    :code:`gid=pi`
        Sets group ownership of the mount to the :code:`pi` group.  This group
        should match the primary group of whatever Linux user is going to be
        running :code:`rph`.

    :code:`mode=755`
        The permissions to apply to the mount.  This value sets
        read/write/execute for the user, and read/execute for everybody else.
        You could modify this (and the :code:`gid` option) if you have multiple
        users who need to run :code:`rph`, but that's out of scope for this
        guide.

    :code:`noatime`
        Disables access-time tracking on the mount.  This provides a
        performance boost in almost all cases, and nothing in :code:`rph`
        depends on atime being available.  If you run into a case where an
        emulator or other tool depends on atime, you can remove this option.

**The trailing 0s** (columns 5 and 6)
    Leave them both as 0.
