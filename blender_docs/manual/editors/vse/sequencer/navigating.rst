
**********
Navigating
**********

Header
======

.. figure:: /images/editors_vse_sequencer_introduction_header.png

   Video Sequencer Header.


View Menu
---------

As usual, the View Menu controls the editor's view settings.

View all Sequences :kbd:`Home`
   Zooms the display to show all strips.
View Selected :kbd:`NumpadPeriod`
   Zooms in the display to fit only the selected strips.
View Frame :kbd:`Numpad0`
   Scrolls the timeline so the current frame is in the center.
Show Seconds :kbd:`Ctrl-T`
   Displays the time instead of the frame number, in the Frame Number Indicator.
Show Frame Number Indicator
   Toggles the units of measure across the bottom of the time cursor between seconds or frames.
Show Offsets
   Shows overflow bars of "extra" content from either cutting or sliding strips.
Waveform Drawing
   Global option to either draw the waveform, or the strip info,
   or use the individual :ref:`strip option <sequencer-sound-waveform>`.
Sync Markers
   Transform Markers as well as Strips.


Markers Menu
------------

:doc:`Markers </animation/markers>` are used to denote frames with key points or significant events
within an animation. Like with most animation editors, markers are shown at the bottom of the editor.

.. figure:: /images/editors_graph-editor_introduction_markers.png

   Markers in animation editor.

For descriptions of the different marker tools see :ref:`Editing Markers <animation-markers-editing>`.


Frame Menu
----------

Preview Range :kbd:`P`, :kbd:`Alt-P`
   See :ref:`graph-preview-range`.
Jump to end of strip :kbd:`PageUp`
   Current frame will jump to end of strip.
Jump to beginning of strip :kbd:`PageDown`
   Current frame will jump to beginning of strip.


Copy and Paste
--------------

Strips can be copied and pasted using the two icon buttons
or through :kbd:`Ctrl-C` and :kbd:`Ctrl-V`.


Refresh Sequencer
-----------------

To force Blender to re-read in files, and to force a re-render of the 3D View,
click the *Refresh Sequencer* button.
Blender will update and synchronize all cached images and compute the current frame.

Certain operations, like moving an object in 3D View, may not force the *Sequencer*
to call for a refresh of the rendered image (since the movement may not affect the rendered image).
If an image or video, used as a strip, is changed by some application outside of Blender,
Blender has no real way of being notified from your operating system.


Backdrop
--------

Displays the current frame in the background of the main view like in the Node editor.


Main View
=========

Adjusting the View
------------------

Use these shortcuts to adjust the sequence area of the VSE:

- Pan: :kbd:`MMB`
- Zoom: :kbd:`Wheel`
- Vertical Scroll: use :kbd:`Shift-Wheel`, or drag on the left scroll bar.
- Horizontal Scroll: use :kbd:`Ctrl-Wheel`, or drag on the lower scroll bar.
- Scale View: :kbd:`Ctrl-MMB` and drag up/down (vertical scale) or left/right (horizontal scale).
- Scale View Vertically: drag on the circles on the vertical scroll bar.
- Scale View Horizontally: drag on the circles on the horizontal scroll bar.


Time Cursor
-----------

To move back and forth through your movie, :kbd:`LMB` click and drag left/right
in the Sequencer's main view by moving the Time cursor (the vertical bar which indicates the current frame).
As you do, the image for that frame is displayed in the Preview region.

When you drag the frame indicator with :kbd:`LMB` directly on a sequence strip,
this will show the strip *solo*, (temporarily disregarding effects and other strips,
showing only this strip's output) and the strip will be highlighted.

When holding :kbd:`Ctrl` while dragging it will snap to the start and endpoints of strips.

Real-time preview is possible on reasonable computers
when viewing an image sequence or movie (``avi``/``mov``) file.
Scene strips can use OpenGL previews or proxies for real-time playback,
otherwise displaying rendered frame is supported, but typically too slow for real-time playback.

.. hint::

   Every other synced editor can be used for scrubbing e.g. the Timeline.
