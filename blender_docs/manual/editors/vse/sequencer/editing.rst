
*******
Editing
*******

Grab/Move
=========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Grab/Move`
   :Hotkey:    :kbd:`G`

Holding down :kbd:`RMB` and then moving the mouse drags the active strip in time or in channels.
Pressing :kbd:`G` moves the all selected strip(s).
Move your mouse horizontally (left/right) to change the strip's position in time.
Move vertically (up/down) to change channels.

Holding down :kbd:`Ctrl` while dragging snaps to the start and endpoints of other strips.
The position of the mouse relative to the selection influences where the strips are snapped.
If it is closer to the start of the selection, then the start frame of the selection gets snapped,
else the end frame will get snapped.

To "ripple edit" (Make room for strips you drag) hold :kbd:`Alt` when placing a strip.

You can also lock the direction to time with :kbd:`X` or to change the strip's channel with :kbd:`Y`.


Start Frame Offset
------------------

The *start frame offset* for that strip could be selected by clicking :kbd:`RMB` on the left arrow of the strip;
holding it down (or pressing :kbd:`G` grab and then moving the mouse left/right)
changes the start frame within the strip by the number of frames you move it.
The frame number label under the strip displays the start frame of the strip.

- If you have a 20-image sequence strip, and drag the left arrow to the right by 10 frames,
  the strip will start at image 11 (images 1 to 10 will be skipped).
  Use this to clip off a roll-up or undesired lead-in.
- Dragging the left arrow left will create a lead-in (copies) of the first frame for as many frames as you drag it.
  Use this when you want some frames for a transition at the start of the clip.


End Frame
---------

The *end frame* of the strip could be selected by clicking :kbd:`RMB` on the right arrow of the strip;
holding it down (or pressing :kbd:`G` grab) and then moving the mouse changes the ending frame within the strip.
The frame number label over the strip displays the end frame of the strip.

- Dragging the right arrow to the left shortens the clip;
  any original images at the tail are ignored. Use this to quickly clip off a roll-down.
- Dragging the right arrow to the right extends the clip.
  For movies and images sequences, more of the animation is used until exhausted.
  Extending a clip beyond its end results in Blender making a copy of the last image.
  Use this for transitions out of this clip.

.. note:: Multiple selection

   You can select several (handles of) strips by :kbd:`Shift-RMB` clicking: when you press :kbd:`G`,
   everything that is selected will move with your mouse- this means that,
   for example, you can at the same time move a strip, shorten two others, and extend a forth one.


Grab/Extend from Frame
======================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Grab/Extend from Frame`
   :Hotkey:    :kbd:`E`

With a number of strips selected, pressing :kbd:`E` lets you interactively extend the strips.
This is similar to grabbing but is useful for extending (or shortening) time around the current frame.

All selected strip handles to the "mouse side" of the current frame indicator will transform together,
so you can change the duration of the current frame.


Slip Strip Content
==================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Slip Strip Content`
   :Hotkey:    :kbd:`S`

The Slip tool allows you to change the position of the contents of a strip without moving the strip itself.


Tools
=====

Erase Strips :kbd:`X`, :kbd:`Delete`
   Delete the selected strip(s).
Duplicate Strips :kbd:`Shift-D`
   Duplicate a strip to make an unlinked copy;
   drag it to a time and channel, and drop it by :kbd:`LMB` click.
Clear Strips Offsets :kbd:`Alt-O`
   To reset the (soft) start/end frame handles.

The Strip Menu contains additional tools for working with strips:

- Insert/Remove Gap
- Deinterlace Movies
- Set Render Size
- Reload Strips
- Swap Inputs
- Lock Strips
- UnLock Strips
- Swap Strips


Snap Strips
===========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Snap Strips`
   :Hotkey:    :kbd:`Shift-S`

Position your cursor (vertical green line) to the time you want.
Snap to current frame to start a strip exactly at the beginning of the frame.
If your Time display is in seconds,
you can get to fractional parts of a second by zooming the display;
you can get all the way down to an individual frame.


Separate Images
===============

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Separate Images`
   :Hotkey:    :kbd:`Y`

For images sequence only -- Converts the strip into multiple strips, one strip for each frame.
Useful for slide shows and other cases where you want to bring in a set on non-continuous images.

Length
   You have to specify the duration you want the resulting strips will be.


Reassign Inputs
===============

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Reassign Inputs`
   :Hotkey:    :kbd:`R`

This tool can be used to assign (reconnect) effect strips in a different way.
Just select three arbitrary strips and press :kbd:`R`.
If you don't create a cycle, those will be connected to a new effect chain.


Cut (soft) at Frame
===================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Cut (soft) at Frame`
   :Hotkey:    :kbd:`K`

This cuts the selected strip in two at the current frame.
This will result in two strips which use the same source, fitting the original strip's timing and length.

.. hint::

   This can be thought of as a quick way to duplicate the current strip,
   adjusting the start/end frames to form two non-overlapping strips showing the same content as before.


Cut (hard) at Frame
===================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Strip --> Cut (hard) at Frame`
   :Hotkey:    :kbd:`Shift-K`

Like *Cut (soft) at Frame*, it cuts a strip in two distinct strips;
however you will not be able to drag the endpoints to show the frames past the cut of each resulting strip.

Although you can adjust the :ref:`duration (hard) <sequencer-duration-hard>`
number buttons in the *Strip Input* panel.

.. hint::

   This can be thought of as a way to simulate splitting the video file in two parts at the cut-point,
   replacing the current strip with each.


Mute
====

Mute Strips :kbd:`H`
   Mute the selected strip(s).
Un-Mute Strips :kbd:`Alt-H`
   Un-Mutes all strips.
Mute Deselected Strips :kbd:`Shift-H`
   You can mute all strips but the selected.


.. _sequencer-edit-change:

Change
======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> Strip Input`
   :Menu:      :menuselection:`Strip --> Change`
   :Hotkey:    :kbd:`C`

The Change sequence operator modifies the file path or effect inputs/type on selected strips.

Effect
   Switch the effects on a selected Effect strip.
Path/Files
   Changes the source file contained in a selected strip.
