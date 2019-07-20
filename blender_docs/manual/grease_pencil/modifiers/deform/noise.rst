
**************
Noise Modifier
**************

The *Noise* Modifier changes the value of one or more stroke/points properties like:
location, strength, thickness or UV texture position
trying to add varied values that make the line unstable and noisy.

Random values can be used for the noise factor for more vivid effects.


Options
=======

.. figure:: /images/grease-pencil_modifiers_deform_noise_panel.png
   :align: right

   Noise Modifier.

Factor
   Strength of the noise effect.

   Random Value
      When enabled, the strength of the noise uses a random value.

   Step
      Number of frames before using a new random value.

Full Stroke
   When enabled, the effect is applied to the stroke as a whole instead of points individually.

Move Extremes
   When disabled, the effect does not affect the stroke start and end points.

Affect
   Combination of stroke/points properties that will be affected by the noise factor.

   Position
      Noise affect the point location.
   Strength
      Noise affect the point strength (opacity).
   Thickness
      Noise affect the point thickness.
   UV
      Noise affect the point UV rotation.


Influence Filters
-----------------

Vertex Group
   Restricts the effect only to a vertex group.

Material
   Restricts the effect only to material that share the same pass index.

Layer
   Restricts the effect only to one layer or to any layers that share the same pass index.
