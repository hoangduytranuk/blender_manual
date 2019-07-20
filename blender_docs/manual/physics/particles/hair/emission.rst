
********
Emission
********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Emission`

.. TODO2.8:
   .. figure:: /images/physics_particles_hair_emission_settings.png

      Hair particle system settings.

Number
   Set the amount of hair strands. Use as little particles as possible,
   especially if you plan to use soft body animation later.
   But you need enough particles to have good control.
   For a "normal" haircut I found some thousand (very roughly 2000) particles to give enough control.
   You may need a lot more particles if you plan to cover a body with fur.
   Volume will be produced later with *Children*.
Hair Length
   Controls how long the hair are.


Source
======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Emission --> Source`

Emit From
   Vertices
      Emits hair particles from the vertices of a mesh.
      When using this the distribution settings (see below) are not available.
   Faces
      Emits hair particles from the surface of a mesh's faces.
   Volume
      Emits hair particles from the volume of an enclosed mesh.

Use Modifier Stack
   Take any :doc:`Modifiers </modeling/modifiers/introduction>` above the Particle Modifier
   in the :ref:`modifier stack <modifier-stack>` into account when emitting particles.

   .. note::

      Note that particles may differ in the final render if these modifiers
      generate different geometry between the viewport and render.

Distribution
   Jittered
      Particles are placed at jittered intervals on the emitter elements.

      Particles/Face
         Number of emissions per face (0 = automatic).
      Jittering Amount
         Amount of jitter applied to the sampling.

   Random
      Particles are emitted from random locations in the emitter's elements.

Random
   Hair particles are emitted in a random order.
Even Distribution
   Hair particle distribution is made even based on surface area of the elements,
   i.e. small elements emit less particles than large elements, so that the particle density is even.
