
***********
Erase Brush
***********

Erase brushes are the special types of brushes that uses *Grease Pencil* for *Erase* tools.
The brush can be changed in the Tool Settings.

Soft and hard eraser brushes are settings variations of the same *Erase Brush*.
you can create many brushes, each with unique settings
to obtain different effects while erasing.

The *Erase Brush* has also other two special eraser types: point and stroke.


Common Options
==============

.. figure:: /images/grease-pencil_modes_draw_brushes_erase-brush-data-block.png
   :align: right

   Brush data-block panel.

Brush
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.

   Add Brush
      When you add a brush, the new brush is a clone of the current one.

.. note::

   In order to save in a blend-user a custom brush, tick Fake User.


Types
=====

Soft/Hard
---------

To simulate a raster type eraser, this eraser type
affects the strength and thickness of the strokes before actually delete a point.

Radius
   The radius of the brush in pixels.

   :kbd:`F` allows you to change the brush size interactively by dragging the mouse/pen or
   by typing a number then confirm.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.
      Occlude Eraser (overlapping squares icon)
         Erase only strokes visible and not occluded by geometry.

Strength
   Control how much will affect the eraser the stroke transparency (alpha).

   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D View and then moving the mouse/pen and then :kbd:`LMB`.
   You can also enter the size numerically.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.

Affect Stroke Strength
   The amount of deletion of the stroke strength (alpha) while erasing.
Affect Stroke Thickness
   The amount of deletion of the stroke thickness while erasing.


Point
-----

Delete one point at a time.

Radius
   Radius of the brush in pixels.

   Use Pressure (pressure sensitivity icon)
      Uses stylus pressure to control how strong the effect is.
   Occlude Eraser (overlapping squares icon)
      Erase only strokes visible and not occluded by geometry.


Stroke
------

Delete an entire stroke.

Radius
   Radius of the brush in pixels.

   Use Pressure (pressure sensitivity icon)
      Uses stylus pressure to control how strong the effect is.
   Occlude Eraser (overlapping squares icon)
      Erase only strokes visible and not occluded by geometry.


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
