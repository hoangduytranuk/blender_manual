.. _bpy.types.TintGpencilModifier:


*************
Tint Modifier
*************

The *Tint* Modifier colorize the original stroke with a tint color.


Options
=======

.. figure:: /images/grease-pencil_modifiers_color_tint_panel.png
   :align: right

   Tint Modifier.

Color
   Defines the tint color for mixing with the original color.

Factor
   Controls the amount for the color mixing.

   A value of 0 respect the original strokes color,
   a value of 1.0 totally replace the original color with the tint color.

   A shift greater than 1.0 will make the points alpha less transparent than originally (2.0 is fully opaque).

Create Materials
   When applied, the modifier will create a new material that will keep the color transformation.

Mode
   The color transformation will be applied on the stroke and/or the fill color.

   Both, Stroke, Fill


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.


Example
=======

.. list-table:: Tint sample.

   * - .. figure:: /images/grease-pencil_modifiers_color_tint_factor-0.png
          :width: 200px

          Color Mix Factor: 0 (original color).

     - .. figure:: /images/grease-pencil_modifiers_color_tint_factor-05.png
          :width: 200px

          Color Mix Factor: 0.5.

     - .. figure:: /images/grease-pencil_modifiers_color_tint_factor-1.png
          :width: 200px

          Color Mix Factor: 1.0 (fully tinted).
