.. _bpy.types.UserPreferencesSystem:

******
System
******

The *System* section allows you to set graphics card options, memory limits & sound settings.

If your hardware does not support some of the options described on this page,
then they will either not show up or be corrected on startup.

.. figure:: /images/editors_preferences_section_system.png

   Preferences System section.


Cycles Render Device
====================

Changes the computing device the :doc:`Cycles </render/cycles/index>` render engine uses to render images.
Cycles can use either the CPU or certain GPU's to render images,
for more information see the :doc:`GPU Rendering </render/cycles/gpu_rendering>` page.

None
   When set to *None* or when the only option is *None*:
   the CPU will be used as the computing device for the Cycles Renderer.
CUDA
   If the system has a compatible NVIDIA CUDA device, it will show up an option for rendering with Cycles.
OpenCL
   If the system has a compatible AMD OpenCL device, it will show up an option for rendering with Cycles.


Memory & Limits
===============

Undo Steps
   Number of Undo steps available.
Undo Memory Limit
   Maximum memory usage in Mb (0 is unlimited).
Global Undo
   This enables Blender to save actions done when you are **not** in *Edit Mode*.
   For example, duplicating Objects, changing panel settings or switching between modes.

   .. warning::

      While disabling this option does save memory,
      it stops the :ref:`Redo Panel <ui-undo-redo-adjust-last-operation>`
      from functioning, also preventing tool options from being changed in some cases.

      For typical usage, its best to keep this enabled.

.. seealso::

   :doc:`Read more about Undo and Redo options </interface/undo_redo>`.

Sequencer Cache Limit
   Upper limit of the Sequencer's memory cache (in megabytes).
   For an optimal Clip editor and Sequencer performance, high values are recommended.
Console Scrollback Lines
   The number of lines, buffered in memory of the console window.
   Useful for debugging purposes and command-line rendering.
Texture Time Out
   Time since last access of a GL texture in seconds, after which it is freed.
   Set this to 0 to keep textures allocated.

   Garbage Collection Rate
      Number of seconds between each run of the GL texture garbage collector.
VBO Time Out
   Time since last access of a GL Vertex buffer object in seconds after which it is freed
   (set to 0 to keep VBO allocated).

   Garbage Collection Rate
      Number of seconds between each run of the GL Vertex buffer object garbage collector.


.. _prefs-system-sound:

Sound
=====

This panel contains the sound settings for live playback
within Blender and are only available with *SDL* or *OpenAL*.
To control these settings for exporting sound
see the :ref:`Encoding Panel <render-output-video-encoding-panel>`
and :ref:`Audio Panel <data-scenes-audio>`.

Audio Device
   Sets the audio engine to use to process and output audio.

   None
      No Audio support (audio strips can still be loaded normally).
   SDL
      Uses Simple Direct Media Layer API from `libsdl.org <https://www.libsdl.org>`__
      to render sounds directly to the sound device output. Very useful for sequencer strips editing.
   OpenAL
      Provides buffered sound rendering with 3D/spatial support.
      Used for 3D source support by *Speaker Objects*.

Channels
   Sets the audio channel count. Available options are:
   *Mono*, *Stereo*, *4 Channels*, *5.1 Surround*, *7.1 Surround*.
Mixing Buffer
   Sets the number of samples used by the audio mixing buffer. Available options are:
   *512*, *1024*, *2048*, *4096*, *8192*, *16384*, and *32768*.
   Higher buffer sizes can cause latency issues,
   but if you hear clicks or other problems, try to increase the size.
Sample Rate
   Sets the audio `sampling rate <https://en.wikipedia.org/wiki/Sampling_(signal_processing)#Sampling_rate>`__.
   Available options are: *44.1 Khz*, *48 Khz*, *96 Khz* and *192 Khz*.
Sample Format
   Sets the audio sample format. Available options are:
   *32 bit float*, *8 bit Unsigned*, *16 Bits Signed*, *24 Bits Signed*,
   *32 Bits Signed*, *32 Bits Float*, and *64 Bits Float*.
