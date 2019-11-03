.. _bpy.types.SmoothGpencilModifier:

***************
Smooth Modifier
***************

The *Smooth* Modifier changes the value of one or more stroke/points properties like:
location, strength, thickness or UV texture position
trying to maintain similar values that make the line fluid and smoother.


Options
=======

.. figure:: /images/grease-pencil_modifiers_deform_smooth_panel.png
   :align: right

   Smooth Modifier.

Factor
   Strength of the smooth effect.

Step
   Number of times to apply the smooth effect.
   High values can reduce the animation performance (FPS).

Affect
   Combination of stroke/points properties that will be affected by the smooth factor.

   Position
      Smooth affect the point location.
   Strength
      Smooth affect the point strength (opacity).
   Thickness
      Smooth affect the point thickness.
   UV
      Smooth affect the point UV rotation.


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.
