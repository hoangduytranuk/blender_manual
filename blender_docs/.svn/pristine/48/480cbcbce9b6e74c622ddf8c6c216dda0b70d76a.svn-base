
********
Children
********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Children`

*Children* are *Hair* and *Keyed* particles assigned subparticles.
They make it possible to work primarily with a relatively low amount of Parent particles,
for whom the physics are calculated. The children are then aligned to their parents.
Without recalculating the physics the number and visualization of the children can be changed.

Children can be emitted from particles or from faces (with some different options).
Emission from *Faces* has some advantages, especially the distribution is more even on each face
(which makes it better suitable for fur and the like).
However, children from particles follow their parents better, e.g.
if you have a soft body animation and do not want the hair to penetrate the emitting mesh.
But see also our manual page about :doc:`Hair </physics/particles/hair/index>`.

If you turn on children the parents are no longer rendered
(which makes sense because the shape of the children may be quite different from that of their parents).
If you want to see the parents additionally turn on the *Parents* button in the *Visualization* panel.

Children carry the same material as their parents and are colored according to the exact
place from where they are emitted (so all children may have different color or other attributes).

The possible options depend from the type of particle system,
and if you work with *Children from faces* or *Children from particles*.
We do not show every possible combination,
only the settings for a *Hair* particle system.


Common Options
==============

Child Type
   None
      No children are generated.
   Simple
      Children are emitted from the parent position.
   Interpolated
      Children are emitted between the *Parent* particles on the faces of a mesh.
      They interpolate between adjacent parents. This is especially useful for fur,
      because you can achieve an even distribution.
      Some of the children can become virtual parents, which are influencing other particles nearby.
Display Amount
   The number of children in the 3D View.
Render Amount
   The number of children to be rendered.
Length
   Length of child paths.
Threshold
   Amount of particles left untouched by child path length.
Seed
   Offset in the random number table for child particles, to get a different randomized result.


Clumping
--------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Children --> Clumping`

Use Clump Curve
   Use :ref:`ui-curve-widget` instead of parameters.
Clump
   Clumping amount along child strands.
   The children may meet at their tip (1.0) or start together at their root (-1.0).
Shape
   Form of *Clump*. Either inverse parabolic (0.99) or exponentially (-0.99).
Twist
   Todo.
Use Twist Curve
   Todo.


Clump Noise
^^^^^^^^^^^

Creates random clumps around the parent hair.

Clump Noise Size
   The size of the clumps.


Roughness
---------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Children --> Roughness`

Use Roughness Curve
   Use :ref:`ui-curve-widget` instead of parameters.
Uniform, Size
   It is based on children location so it varies the paths in a similar way when the children are near.
Endpoint, Shape
   "Rough End" randomizes path ends (a bit like random negative clumping).
   Shape may be varied from <1 (parabolic) to 10.0 (hyperbolic).
Random, Size, Threshold
   It is based on a random vector so it is not the same for nearby children.
   The threshold can be specified to apply this to only a part of children.
   This is useful for creating a few stray children that will not do what others do.


Kink
----

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Children --> Kink`

.. _fig-particle-child-kink:

.. figure:: /images/physics_particles_emitter_children_kink.png

   Child particles with Kink.

   From left to right: Curl, Radial, Wave, Braid, Spiral.

With *Kink* you can rotate the children around the parent.
See Fig. :ref:`fig-particle-child-kink` above picture for the different types of *Kink*.

Kink Type
   Nothing
      Deactivated.
   Curl
      Children grow in a spiral around the parent hairs.
   Radial
      Children form around the parent a wave shape that passes through the parent hair.
   Wave
      Children form a wave, all in the same direction.
   Braid
      Children braid themselves around the parent hair.
   Spiral
      Generates a spiral at the end of each hair.

      Radius, Resolution
         Define the overall size.
      Shape
         Makes a the spiral grow in- or outward.

   .. note:: Alignment Limitations

      When hair is pointing straight up (along the chosen spiral axis, default Z), spirals may not show up!
      This is a limitation of the projection method used.
      Giving a slight tilt or random orientation to hairs fixes this.

Amplitude
   The amplitude of the offset.
Clump
   How much clump effects kink amplitude.
Flatness
   How flat the hairs are.

Frequency
   The frequency of the offset (1/total length). The higher the frequency the more rotations are done.
Shape
   Where the rotation starts (offset of rotation).


Simple
======

Size
   Only for *Emitter*. A multiplier for children size.
Random Size
   Random variation to the size of child particles.

Radius
   The radius in which the children are distributed around their parents.
   This is 3D, so children may be emitted higher or lower than their parents.
Roundness
   The roundness of the children around their parents. Either in a sphere (1.0) or in-plane (0.0).


Interpolated
============

Virtual Parents
   Relative amount of virtual parents.
Long Hair
   Calculate children that suit long hair well.


Parting
-------

TODO.


Example
=======

.. figure:: /images/physics_particles_emitter_children_round-clump.png

   From left to right: Round: 0.0, Round: 1.0, Clump: 1.0, Clump: -1.0, Shape: -0.99.
