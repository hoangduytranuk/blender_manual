.. _bpy.types.OpacityGpencilModifier:


****************
Opacity Modifier
****************

The *Opacity* Modifier change the opacity (alpha) value of the stroke points.

The alpha value in *Grease Pencil* is stored per-point,
The modifier can alter these values to go from totally transparent points to totally opaque points.


Options
=======

.. figure:: /images/grease-pencil_modifiers_color_opacity_panel.png
   :align: right

   Opacity Modifier.

Factor
   Controls the Opacity (Alpha) value of the stroke points.

   A value of 1.0 respect the original alpha value of the points,
   a shift less than 1.0 make the points more transparent than originally,
   and a shift greater than 1.0 make the points more opaque than originally.

   Sets value to 2.0 makes the points alpha fully opaque.

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

.. list-table:: Factor Opacity samples.

   * - .. figure:: /images/grease-pencil_modifiers_color_opacity_factor-03.png
          :width: 200px

          Opacity Factor: 0.3.

     - .. figure:: /images/grease-pencil_modifiers_color_opacity_factor-1.png
          :width: 200px

          Opacity Factor: 1.0 (original alpha).

     - .. figure:: /images/grease-pencil_modifiers_color_opacity_factor-2.png
          :width: 200px

          Opacity Factor: 2.0 (fully opaque).
