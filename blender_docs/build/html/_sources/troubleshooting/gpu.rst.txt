
*****************
Graphics Hardware
*****************

Blender uses of OpenGL for the 3D viewport and user interface.
The graphics card (GPU) and driver have a big impact on Blender's behavior and performance.

This page lists possible solutions for graphics glitches, problems with Eevee and Cycles,
and crashes related to your GPU.


Drivers
=======

Upgrading to the latest graphics drivers often solves problems.
Newer drivers have bug fixes that help Blender function correctly.


Windows
-------

On Windows drivers are provided by the graphics card manufacturer (Intel, AMD and NVIDIA).
Windows update automatically installs graphics drivers,
or your computer manufacturer may provide its own version of the graphics drivers.
However these are not always the latest version or may have been corrupted in some way.

To ensure you have the latest version, go to the graphics card manufacturer's website and
download the latest drivers from there. It can help to uninstall the previous drivers first and
perform a clean installation.


Linux
-----

On Linux, graphics drivers are usually installed as a package by your Linux distribution.
Installing the latest drivers is typically done by upgrading packages or the distribution as a whole.
Some distributions provide multiple packages for multiple drivers versions,
giving you the choice to install newer versions.

For NVIDIA there are open source (Nouveau) and closed source (by NVIDIA) graphics drivers.
Blender functions best with the closed source drivers as they are more optimized and complete.
Linux graphics drivers can be downloaded from NVIDIA's website, however in most cases
the ones from your Linux distribution are fine and make things easier.
Manually downloading drivers is mostly useful to get the very latest version,
for example for a GPU that was only recently released.

For AMD the drivers are open source, except for the OpenCL support which is available as part of Pro drivers.
Installing packages through your Linux distribution is usually best.
AMD also provides graphics drivers for download on their website if you need the latest version.


macOS
-----

On macOS graphics drivers are built into the operating system and
the only way to get newer drivers is to upgrade macOS as a whole to the latest version.


Laptops
=======

Laptops often have two GPUs for power saving purposes.
One slower onboard GPU (typically Intel) and one faster dedicated GPU for a better performance (AMD or NVIDIA).

For the best performance the dedicated GPU should be used for Blender.
Which GPU to use for which application can be configured in your graphics driver settings.

If there is a graphics glitch specific to the onboard GPU, then using the dedicated GPU can also help avoid that.


Common Problems
===============

Unsupported Graphics Driver Error
---------------------------------

This means your graphics card and driver do not have the minimum required OpenGL 3.3 version needed by Blender.

Installing the latest driver can help upgrade the OpenGL version,
though some graphics cards are simply too old to run the latest Blender.
Using Blender 2.79 or earlier is the only option then.


Crash on Startup
----------------

Try running Blender from the :doc:`command line </advanced/command_line/index>`,
to see if any helpful error messages are printed.

On Windows, graphics drivers can sometimes get corrupted.
In this case it can help to uninstall all graphics drivers (there may be multiple from Intel, AMD and NVIDIA) and
perform a clean installation with drivers from the manufacturer's website.


Poor Performance
----------------

- Update your graphics drivers (see above).
- On laptops, make sure you are using a dedicated GPU (see above).
- Try lowering quality settings in :menuselection:`Preferences --> System --> Memory & Limits`.
- Try undoing settings in your graphics drivers, if you made any changes there.


Render Errors
-------------

See :doc:`Eevee </render/eevee/limitations>` and
:doc:`Cycles </render/cycles/gpu_rendering>` documentation respectively.


Wrong Selection in 3D Viewport
------------------------------

See :ref:`Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>`.


Information
===========

To find out which graphics card and driver Blender is using,
use :menuselection:`Help --> Save System Info` inside Blender.
The OpenGL section will have information about your graphics card, vendor and driver version.
