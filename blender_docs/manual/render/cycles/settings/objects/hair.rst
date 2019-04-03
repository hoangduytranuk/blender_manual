
**************
Hair Particles
**************

These are extra settings for :doc:`Hair Particles </physics/particles/hair/index>` used by Cycles.

.. seealso::

   There are also scene level hair settings which can be found with
   the :ref:`Geometry <cycles-settings-scene-render-geometry>` settings.


Hair Settings
=============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Cycles Hair Settings`

The Cycles Hair Settings, under the particle tab, are used to control each hair particle system's strand properties.

Shape
   A shape parameter that controls the transition in thickness between the root and tip.
   Negative values make the primitive rounded more towards the top,
   the value of zero makes the primitive linear,
   and positive values make the primitive rounded more towards the bottom.


Thickness
---------

Root
   Multiplier of the hair width at the root.
Tip
   Multiplier of the hair width at the tip.
Scaling
   Multiplier for the *Root* and *Tip* values. This can be used to change the thickness of the hair.

   .. Particle width scaling relative to the object scale.

Close tip
   Sets the thickness at the tip to zero, even when using a non-zero tip multiplier.
