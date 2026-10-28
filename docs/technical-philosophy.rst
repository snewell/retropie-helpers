Technical Philosophy
====================
The technical philosophy of this project is to largely apply the Unix Philosophy
to a dedicated emulation box.  The goal is to sand down a few rough edges and
pain points, while also providing enough infrastructure and hooks to make the
project extremely flexible and easy to build on.

Tools do One Thing
------------------
Every script has exactly one job.  Whether it's injecting extra retroarch config
files, patching files, or working around an upstream bug.  This makes it very
easy to put scripts together in different ways.  As a practical example,
:code:`xdelta-patcher` is used for PS1, PS2, PSP, Gamecube, Wii, Dreamcast, and
Sega CD games.

"One Thing" *may* mean that a script's job is just to piece together other
scripts into a chain.  This is how the launch scripts work, as well as
:code:`retroarch-orchestrator`.

Configuration is Separate
-------------------------
Configuration is managed via rc files, so you have the full power of bash.  Most
users will never need this, but it does make edge cases much simpler to solve.
Instead of digging through Python to add features or handle unique situations,
it's programmable via bash and translated into standard CLI options.  The big
advantage here is that enhancements to the tooling should be applicable to
pretty much every user, since custom behavior is handled locally.

It's (mostly) Purely Additive
-----------------------------
Changes to retropie defaults are minimal (the biggest one being a replacement
of retroarch with a wrapper).  The goal isn't to compete or fight with
retropie's automation (which is fantastic), it's to build on it.  As much as
possible, this project should be a drop-in enhancement that builds on the
amazing upstream foundation.
