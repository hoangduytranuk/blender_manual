.. _bpy.types.MultiplyGpencilModifier:

****************
Multiple Strokes
****************

The *Multiple Strokes* modifier generate multiple parallel strokes around the original ones.


Options
=======

.. figure:: /images/grease-pencil_modifiers_generate_multiple-strokes_panel.png
   :align: right

   The Multiple Strokes modifier.

Duplications
   The number of additional strokes.

Distance
   Distance between the original and the duplicate strokes.

Offset
   Control the offset position (inner or outer) for duplicate strokes.

Enable Fading
   When activated, the duplicate strokes fades out using their opacity or thickness.

   Center
      Control the initial position for the fading.

   Thickness
      Fade influence on strokes thickness.

   Opacity
      Fade influence on strokes opacity.

Angle Splitting
   When activated, divide the resulting duplicate strokes at certain angles.

      Angle
         Angle to split the strokes.


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.
