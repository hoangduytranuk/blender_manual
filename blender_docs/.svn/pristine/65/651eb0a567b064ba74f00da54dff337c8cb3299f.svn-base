
**************
Screen Capture
**************

Screenshots
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Window --> Save Screenshot`
   :Hotkey:    :kbd:`Ctrl-F3`

.. figure:: /images/editors_info_screen-capture_save-options.png

   Save Screenshot option.

:kbd:`Ctrl-F3` will take a screenshot of Blender and then open the :doc:`File Browser </editors/file_browser/index>`,
allowing you to specify the name and location of the screenshot.
In the example image at the right, the ``PNG`` format will be the output of the screenshot taken
(settings are the same as the ones available to save render results).
When the :doc:`File Browser </editors/file_browser/index>` opens, on the left, there is a tab
called *Save Screenshot* where you can find format settings and a checkbox with the option
*Full Screen*.

- Check the Option to save the entire Blender window
  (full width and height of the Blender window you are using when you call the command).
- Uncheck the box to save only your active area (where your mouse is located when you call the command).


.. _info-screencast:

Screencasts
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Window --> Make Screencast`
   :Hotkey:    :kbd:`Alt-F3`

This is a quick way to make screencasts from within Blender.

.. note::

   This is limited to a single window and does *not* support audio.

   For recording tutorials you may want to use more comprehensive, 3rd party solutions.

Screencasts will record your actions over time either as a video or sequence of image files.
The type and location of the output are determined by the settings
in the :doc:`Output panel </render/output/output>` of the Properties :ref:`Render tab <properties-render-tab>`.
The default settings will generate a screencast consisting of a series of ``PNG`` images captured
every 50 ms and stored in the ``/tmp`` folder. If you want to record a video,
set the *Output* to one of the *Movie File Formats* supported by your system
listed in the *Output panel* format menu.
If you are unsure what video codecs your system supports, select ``AVI JPEG``.

.. note::

   You can change the frame rate for a screencast in the :ref:`User Preferences <prefs-system-screencast>`.

When you start Blender Screencasts, the header of the *Info Editor* will change,
and it will show you a button for stopping your capture.

.. figure:: /images/editors_info_screen-capture_stop-button.png

   Info Header with the Capture Stop button.

.. note:: The Only Way to Stop the Screencast

   Pressing the Stop button in the header of the Info Editor is the only way to stop the Screencast capture.
   If you press :kbd:`Esc`, the shortcut will only work for operations
   performed in the Blender *User Interface*, (it will stop animations, playbacks and so on...),
   but will not work to stop *Screencasts*.

.. _fig-screencast-frame-range:

.. figure:: /images/editors_info_screen-capture_frame-range.png

   :menuselection:`Render --> Dimensions Panel --> Frame Range`

The frames are stored using a suffix added to their file name,
where the suffix is composed of the numbers present in the fields for *start* and *end frames*,
defined in the Frame Range of the Dimensions panel,
:ref:`Render tab <properties-render-tab>`
(see Fig. :ref:`fig-screencast-frame-range` highlighted in yellow).

.. note::

   The configuration of the End frame, present in the Frame Range of the Dimensions Panel,
   **will not** stop your capture automatically.
   You will always have to stop the Screencast manually, using the Stop button.

The Videos are generated internally in the same manner as the *Screenshots*,
using the width and height of the Window you are working in.
If you choose to capture to a Video file,
Blender will have to pass those frames to a Video codec.

.. warning::

   Some codecs limit the output width/height or the video quality:

   - When you save your *Screencast* in an Image format,
     the Images will be saved using the entire Blender Window, with full width and height,
     and the quality of the Image will be defined by its type (e.g. JPG, PNG, and so on)
     and configuration (e.g. Slider *quality* of the .JPG format).
   - When you save your *Screencast* in a Video format, it will be sent to a codec.
     Depending on the codec limitations, the resulting output Video could be scaled down.
     Furthermore, some combinations of Window width and height cannot be processed by certain codecs.
     In these cases, the *Screencast* will try to start, but will immediately stop.
     In order to solve this, choose another Window format and/or another codec.


Blender Window Dimension
------------------------

There is a way to match the Blender Window dimensions with the Output Video File,
achieving standard dimensions for the output of the Blender Screencast
(e.g. NTSC, HD, Full HD, etc.).
You can control the width and height of your Blender Window, starting Blender from a command line.
To learn more about starting Blender from a command line,
see the page about the :doc:`Blender Console Window </advanced/command_line/introduction>`.
