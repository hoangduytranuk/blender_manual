.. _gpencil_sculpt-toolbar-index:

***************
Sculpting Tools
***************

For *Grease Pencil* Sculpt modes each brush type is exposed as a tool,
the brush can be changed in the Tool Settings.
See :doc:`Brush </grease_pencil/modes/sculpting/tool_settings/brush>` for more information.

Grease Pencil sculpt tools:

.. figure:: /images/grease-pencil_modes_sculpting_toolbar_brushes.png
   :align: right

   3D View Mode selector: Sculpt Mode.

.. note::

   Some :ref:`Object Mode <object-toolbar-index>` are also present.

:ref:`Select <tool-select-tweak>`
   Select or moved.

   :ref:`Select Box <tool-select-box>`
      Select geometry by dragging a box.
   :ref:`Select Circle <tool-select-circle>`
      Select geometry by painting on it.
   :ref:`Select Lasso <tool-select-lasso>`
      Select geometry by drawing a lasso.

Smooth
   Eliminates irregularities in the area of the drawing
   within the brush’s influence by smoothing the positions of the points.

Thickness
   Increase or decrease the points thickness in the area of the drawing
   within the brush’s influence.

Strength
   Increase or decrease the points transparency (alpha) in the area of the drawing
   within the brush’s influence.

Randomize
   Add noise to the strokes in the area of the drawing
   within the brush’s influence by moving points location in a random way.

Grab
   Used to drag a group of points around. Unlike the other brushes,
   Grab does not modify different points as the brush is dragged across the model.
   Instead, Grab selects a group of points on mouse-down, and pulls them to follow the mouse.
   The effect is similar to moving a group of points in Edit Mode with Proportional Editing enabled.

Push
   Moves points in the direction of the brush stroke.

Twist
   Twist the points in counter-clockwise (CCW) or Clockwise (CW) rotation.

Pinch/Inflate
   Pulls points towards the center of the brush.
   The inverse setting is Inflate, in which points are pushed away from the center of the brush.

Clone
   Adds copies of the strokes in the clipboard in the center of the brush.
   You have to copy the selected strokes you want into the clipboard with :kbd:`Ctrl-C` before using the tool.
