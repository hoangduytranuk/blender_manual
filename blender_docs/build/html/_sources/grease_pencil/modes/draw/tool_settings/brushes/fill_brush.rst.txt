
**********
Fill Brush
**********

Fill brushes are the special type of brushes that uses *Grease Pencil* for the *Fill* tools.
The brush can be changed in the Tool Settings.

The different fill brushes are settings variations of the same *Fill Brush*.
you can create many brushes, each with unique settings
to obtain different result when filling areas.


Common Options
==============

.. figure:: /images/grease-pencil_modes_draw_brushes_fill-brush-data-block.png
   :align: right

   Brush data-block panel.

Brush
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.

   Add Brush
      When you add a brush, the new brush is a clone of the current one.

.. note::

   In order to save in a blend-user a custom brush, tick Fake User.

Leak Size
   Size in pixel to consider the leak as closed.

Thickness
   The thickness radius of the boundary stroke in pixels.

Simplify
   Number of simplify steps to apply to the boundary line.
   Higher values reduce the final filled area's accuracy.

Boundary
   Sets the type of fill boundary limits calculation to perform.

   Default
      Use the thickness of the strokes and the editing lines together.
   Stroke
      Use only the thickness of the strokes (ignore edit lines).
   Line
      Use only the edit lines (ignore strokes).
   Show lines (grid icon)
      Toggle show help lines to see the fill boundary.


Display
=======

Icon
   Sets a predefined icon to use.

Custom Icon
   Allows definition of a custom brush icon.

   Image Path
      Defines the path to the image to use as custom icon.

Show Brush
   Shows the brush shape in the viewport.

Color
   Set the color of the brush ring.
