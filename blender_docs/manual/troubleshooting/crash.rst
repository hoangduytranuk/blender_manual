
*******
Crashes
*******

The most common causes of Blender crashes:

- Running out of memory.
- Issues with graphics hardware or drivers.
- Bugs in Blender.

Firstly, you may be able to recover your work with :menuselection:`File --> Recover --> Auto Save...`.

To prevent the problem from happening again, you can check that the graphics drivers are up to date, upgrade your
machine's hardware (the RAM or graphics card), and disable some options that are more memory intensive:

- Reduce undo steps
  :menuselection:`Preferences --> System --> Memory & Limits --> Undo Steps`.
- Using multisample anti-aliasing also increases the memory usage and makes the display slower.
- On Linux, the Window Manager (KDE, Gnome, Unity) may be using hardware accelerated effects
  (e.g. window shadows and transparency) that are using up the memory that Blender needs.
  Try disabling the desktop effects or switch to a lightweight Window Manager.


Crash Log
=========

When Blender crashes, it writes out a text file
which contains information that may help identify the cause of the crash.

On a crash, a file is written based on the name of the currently loaded blend-file,
so ``test.blend`` will create a file called ``test.crash.txt``.
The crash log for unsaved files will be written into the :ref:`temp-dir` directory.

This file contains a log of tools used up until the crash as well as some other debug information.

When reporting bugs on crashes it can be helpful to attach this file to your reports,
especially when others are unable to reproduce the crash.

.. warning::

   This is currently disabled for Windows.
