
***************
Animation Tools
***************

.. _bpy.ops.gpencil.blank_frame_add:

Insert Blank Keyframe
=====================

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode, Edit Mode, Sculpt Mode
   :Menu:      :menuselection:`Stroke --> Animation --> Insert Blank Keyframe`

Add a new blank keyframe to the active layer at the current frame.
If there is already a keyframe at the current frame,
a new blank keyframe will be added on the next frame.

All Layers
   When enabled, Blank keyframe will be created on all layers, not only the active one.


.. _bpy.ops.gpencil.active_frames_delete_all:

Delete Frame(s)
===============

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode, Edit Mode, Sculpt Mode
   :Menu:      :menuselection:`Stroke --> Animation --> Delete Frame(s)`

Deletes the last keyframe in the Dope Sheet or the current keyframe if you are on one.


.. _bpy.ops.gpencil.frame_duplicate:

Duplicate
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode, Edit Mode, Sculpt Mode
   :Menu:      :menuselection:`Stroke --> Animation --> Duplicate Active Frame, Duplicate All Layers`

Duplicates the strokes on the last keyframe by copying them to the current frame.

Mode
   Active
      Duplicate only the active layer.

   All
      Duplicate all the layers.


Interpolation
=============

.. _bpy.ops.gpencil.interpolate:

Interpolate
-----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode, Edit Mode, Sculpt Mode
   :Menu:      :menuselection:`Stroke --> Animation --> Interpolate --> Interpolate`
   :Hotkey:    :kbd:`Ctrl-Alt-E`

Interpolates strokes between the previous and next keyframe by adding a *single* keyframe.
When you are on a frame between two keyframes and press :kbd:`Ctrl-Alt-E` a new breakdown keyframe
will be added. This way you define the final interpolation for the new stroke.


.. _bpy.ops.gpencil.interpolate_sequence:

Sequence
--------

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode, Edit Mode, Sculpt Mode
   :Menu:      :menuselection:`Stroke --> Animation --> Interpolate --> Sequence`
   :Hotkey:    :kbd:`Shift-Ctrl-E`

Interpolate strokes between the previous and next keyframe by adding *multiple* keyframes.
A breakdown keyframe will be added on every frame between the previous and next keyframe.

.. note::

   The *Interpolate* and *Sequence* tools work better when the strokes in the previous and next keyframes
   have the same amount of points. For example when there are duplicated strokes on different keyframes
   only with different location, rotation or scale.
