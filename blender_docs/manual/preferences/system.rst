.. _bpy.types.UserPreferencesSystem:

******
System
******

The *System* tab allows you to set resolution, scripting console preferences,
sound, graphics cards, and internationalization.

If your hardware does not support some of the options described on this page,
then they will either not show up or get corrected on startup.
If this happens do not worry, you can either consult your computer manual
to find a supported value or just let Blender correct it.

.. figure:: /images/preferences_system_tab.png

   User Preferences System tab.


General
=======

.. _preferences-system-general-frame-server-port:

Frame Server Port
   TCP/IP port used in conjunction with the IP Address of the machine for frameserver rendering.
   Used when working with distributed rendering.
   Avoid changing this port value unless it is conflicting with already
   existing service ports used by your Operating System and/or other software.
   Always consult your operating system documentation and services or
   consult your system administrator before changing this value.
Console Scrollback
   The number of lines, buffered in memory of the console window.
   Useful for debugging purposes and command-line rendering.


.. _prefs-system-sound:

Sound
=====

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


Sound Options
-------------

These settings control how sound behaves during live playback
within Blender and are only available with *SDL* or *OpenAL*.
To control these settings for exporting sound see the
:ref:`Encoding Panel <render-output-video-encoding-panel>`
and :ref:`Audio Panel <data-scenes-audio>`.

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


.. _prefs-system-screencast:

Screencast
==========

These settings are used to control the frame rate for recording a :ref:`Screencast <info-screencast>`.

FPS
   The frame rate for screencast playback.
Wait Timer
   Time in milliseconds between each frame recorded for screencast.


Compute Device
==============

The *Compute Device* option allows the user to change the computing device
the :doc:`Cycles </render/cycles/index>` render engine uses to render images.
Cycles can use either the CPU or certain GPU's to render images,
for more information see the :doc:`GPU Rendering </render/cycles/gpu_rendering>` page.

None
   When set to *None* or when the only option is *None*:
   the CPU will be used as the computing device for the Cycles Renderer.
CUDA
   If the system has a compatible Nvidia CUDA enabled graphics card you will be able
   to use it to render with the :doc:`Cycles </render/cycles/features>` render engine.
OpenCL
   If the system has a compatible AMD OpenCL device, it will show up an option for rendering with Cycles.


.. _prefs-system-opensubdiv:

OpenSubdiv Compute
==================

The options here will set the compute device used by OpenSubdiv for
the :doc:`Subdivision Surface Modifier </modeling/modifiers/generate/subsurf>`.

None
   Disables any OpenSubdiv compute devices, makes sure legacy subdivision method is used.
   Use this option when OpenSubdiv causes any bugs or regressions.
CPU
   Single threaded CPU implementation.
   It is mainly useful in cases when GPU compute is possible and threaded CPU option causes artifacts
   (it is unlikely to happen, but still possible).
OpenMP
   Multi-threaded CPU implementation. Use it for maximum performance in cases when GPU compute is not available.
GLSL Transform Feedback
   Uses GPU to perform calculations, has minimal requirements to video card and driver.
GLSL Compute
   Uses GPU to perform calculations, supposed to be more efficient than *Transform Feedback*
   but also has higher requirements to video card and driver.


OpenGL
======

Clip Alpha
   Clip alpha below this threshold in the 3D View.
   Note that the default is set to a low value to prevent issues on some GPU's.
Mipmaps
   Scale textures for 3D View using :term:`mip-map` filtering. This increases display quality, but uses more memory.
GPU Mipmap Generation
   Generate mip-maps on the GPU instead of the CPU.
16 Bit Float Textures
   Enables the use of 16 Bit per component Texture Images (floating point images).
Selection
   Selection method to use for selecting.

   Automatic
      Automatically chooses the best setting depending on your OS, GPU, and drivers.
   OpenGL Select
      Legacy OpenGL selection method for legacy hardware.
   OpenGL Occlusion Queries
      More optimized OpenGL selection method.
      Use this method if you are using an `OpenSubdiv Compute`_ compute device.

OpenGL Depth Picking
   This option uses an alternative method of picking which uses depth information to select the front-most elements.
   It is only used for selecting with the cursor (not border select, lasso, circle select, etc.).

   Performance varies depending on your OpenGL hardware and drivers.
Anisotropic Filtering
   Sets the level of anisotropic filtering.
   This improves the quality of how textures are drawn at the cost of performance.
   Available Options are: *Off* (No Filtering), *2x*, *4x*, *8x*, and *16x*.


.. _prefs-system-window-draw:

Window Draw Method
==================

Window Draw Method
   Specifies the Window Draw Method used to display Blender Window(s).

   Automatic
      Automatically set based on graphics card and driver.
   Triple Buffer
      Use a third buffer for minimal redraws at the cost of more memory.
      If you have a capable GPU, this is the best and faster method of redraw.
   Overlap
      Redraw all overlapping regions. Minimal memory usage, but more redraws.
      Recommended for some graphics cards and drivers combinations.
   Overlap Flip
      Redraw all overlapping regions. Minimal memory usage, but more redraws (for graphics drivers that do flipping).
      Recommended for some graphic cards and drivers combinations.
   Full
      Do a full redraw each time. Only use for reference, or when all else fails.
      Useful for certain cards with bad to no OpenGL acceleration at all.

.. _prefs-system-multi-sampling:

Multi-Sampling
   This enables :term:`FSAA` for smoother drawing, at the expense of some performance.

   .. note::

      This is known to cause selection issues on some configurations,
      see: :ref:`troubleshooting-3dview-invalid-selection`.

Region Overlap
   This checkbox will enable Blender to draw regions overlapping the 3D View.
   It means that the *Tool Shelf* and *Properties regions*,
   will be drawn overlapping the 3D View editor.

   If you have a capable graphics card and drivers with *Triple Buffer* support,
   clicking the checkbox will enable the overlapping regions to be drawn using the *Triple Buffer* method,
   which will also enable them to be drawn using Alpha, showing the 3D View contents through the regions.

Text Draw Options
   Enable interface text anti-aliasing.
   When disabled, texts are drawn using text straight render (filling only absolute pixels).


Textures
========

Limit Size
   Limit the maximum resolution for pictures used in textured display to save memory.
   The limit options are specified in a square of pixels
   (e.g: the option 256 means a texture of 256×256 pixels). This is useful for game engineers,
   whereas the texture limit matches paging blocks of the textures in the target graphic card memory.
   Available Options are: *Off* (No limit), *128*, *256*, *512*, *1024*, *2048*, *4096*, and *8192*.
Time Out
   Time since last access of a GL texture in seconds, after which it is freed. Set to 0 to keep textures allocated.
   Minimum: *0*, Maximum: *3600*.
Collection Rate
   Number of seconds between each run of the GL texture garbage collector.
   Minimum: *0*, Maximum: *3600*.

Image Draw Method
   Method to draw images as the following options are supported:

   2D Texture
      Uses CPU for display transform and draws images as a 2D texture.
   GLSL
      Fastest method using GLSL for display transform and draws images as a 2D texture.
   Draw Pixels
      Uses CPU for display transform and draws images as a 2D texture.


Sequencer/Clip Editor
=====================

Memory Cache Limit
   Upper limit of the Sequencer's memory cache (megabytes).
   For optimum Clip editor and Sequencer performance, high values are recommended.


.. _bpy.types.UserSolidLight:

Solid OpenGL Lights
===================

*Solid OpenGL Lights* are used to light the 3D View,
mostly during *Solid view*. Lighting is constant and position "world" based.
There are three virtual light sources, also called OpenGL auxiliary lamps,
used to illuminate 3D View scenes, which will not display in renders.

The Lamp icons allow the user to enable or disable OpenGL lamps.
At least one of the three auxiliary OpenGL Lamps must remain enabled for the 3D View.
The lamps are equal, their difference is their positioning and colors.
You can control the direction of the lamps, as well as their diffuse and specular colors.

Use
   Toggles the specific lamp.
Diffuse
   This is the constant color of the lamp.
Specular
   This is the highlight color of the lamp.
Direction
   Clicking with :kbd:`LMB` in the sphere and dragging the mouse cursor
   let us the user change the direction of the lamp by rotating the sphere.
   The direction of the lamp will be the same as shown at the sphere surface.


Color Picker Type
=================

Choose which type of :term:`color space` you prefer. It will show when clicking :kbd:`LMB` on any color button.

See the different color picker types at the :doc:`Color picker </interface/controls/templates/color_picker>` page.


.. _prefs-system-weight:

Custom Weight Paint Range
=========================

*Mesh skin weighting* is used to control how much a bone deforms the mesh of a character.
To visualize and paint these weights, Blender uses a color ramp (from blue to green, and from yellow to red).
Enabling the checkbox will enable an alternate map using a ramp starting with an empty range.
Now you can create your custom map using the common color ramp options.
For detailed information see the :doc:`Color ramps </interface/controls/templates/color_ramp>` page.


Fonts
=====

Interface Font
--------------

Interface Font
   Replacement for the default user interface font.
Mono-space Font
   Same as above for the mono-space font.


.. _prefs-system-international:

Internationalization
--------------------

Blender supports a wide range of languages,
enabling this checkbox will enable Blender to support International Fonts.
International fonts can be loaded for the User Interface and used instead of Blender default bundled font.

This will also enable options for translating the User Interface
through a list of languages and Tips for Blender tools which appear
whenever the user hovers a mouse over Blender tools.

Blender supports I18N for internationalization.
For more Information on how to load International fonts,
see: :doc:`Editing Texts </modeling/texts/selecting_editing>` page.
