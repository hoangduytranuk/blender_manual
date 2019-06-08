
******
Render
******

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Render`

The Render Panel controls how particles appear when they are rendered.

.. TODO2.8 Add warning.

   Cycles support only Object and Group render types. (T48467)

Material Index
   Set which of the object's materials is used to shade the particles.
Parent
   Use a different object's coordinates to determine the birth of particles.

Emitter
   When disabled, the emitter is no longer rendered. Activate the button *Emitter* to also render the mesh.
Parents
   Render also parent particles if child particles are used.
   Children have a lot of different deformation options,
   so the straight parents would stand between their curly children.
   So by default *Parents* are not rendered if you activate *Children*.
   See :doc:`Children </physics/particles/emitter/children>`.

Unborn
   Render particles before they are born.
Died
   Render particles after they have died.
   This is very useful if particles die in a collision *Die on hit*, so you can cover objects with particles.


Type
====

None
----

When set to *None*, particles are not rendered.
This is useful if you are using the particles to duplicate objects.


.. _particle-halo:

Halo
----

Halo are rendered as glowing dots or a little clouds of light.
Although they are not really lights because they do not cast light into the scene like a lamp.
They are called *Halos* because you can see them, but they do not have any substance.

Trail Count
   Set the number of trail particles. When greater than 1, additional options appear.
Length in Frames
   Path timing is in absolute frames.
Length
   End time of drawn path.
Random
   Give path lengths a random variation.


Line
----

The Line visualization mode creates (more or less thin)
polygon lines with the strand renderer in the direction of particles velocities. The thickness
of the line is set with the parameter *Start* of the *Strands* shader
(*Material* tab, *Links and Pipeline* panel).

Tail
   Set the length of the particle's tail.
Head
   Set the length of the particle's head.
Speed
   Multiply the line length by particles' speed. The faster, the longer the line.

Trail Count
   See description in `Halo`_.


Path
----

.. figure:: /images/physics_particles_emitter_render_path.png

   The Visualization panel for Path visualization.

The *Path* visualization needs a :doc:`Hair </physics/particles/hair/index>` particle system or
:doc:`Keyed </physics/particles/emitter/physics/keyed>` particles.

Strand render
   [Keypointstrands] Use the strand primitive for rendering. Very fast and effective renderer.
Adaptive render
   Tries to remove unnecessary geometry from the paths before rendering particle strands in
   order to make the render faster and easier on memory.

   Angle
      How many degrees path has to curve to produce another render segment
      (straight parts of paths need fewer segments).
   Pixel
      How many pixels path has to cover to produce another render segment
      (very short hair or long hair viewed from far away need fewer parts).
      (only for Adaptive render).

B-Spline
   Interpolate hair using B-Splines.
   This may be an option for you if you want to use low *Render* values.
   You loose a bit of control but gain smoother paths.
Steps
   Set the number of subdivisions of the rendered paths (the value is a power of 2).
   You should set this value carefully,
   because if you increase the render value by two you need four times more memory to render.
   Also the rendering is faster if you use low render values (sometimes drastically).
   But how low you can go with this value depends on the waviness of the hair (the value is a power of 2).
   This means 0 steps give 1 subdivision,
   1 give 2 subdivisions, 2 --> 4, 3 --> 8, 4 --> 16, ... *n* --> *n*\ :sup:`2`.


Timing
^^^^^^

Absolute Path Time
   Path timing is in absolute frames.
Start
   Start time of the drawn path.

   .. Ed: option is missing instead: Trail count

End
   End time of the drawn path.
Random
   Give the path length a random variation.

.. Todo 2.8
   (old) Please see also the manual page about
   :doc:`Strands </render/blender_render/materials/properties/strands>` for an in-depth description.


Object
------

Dupli Object
   The specified object is duplicated in place of each particle.

Global
   Use object's global coordinates for duplication.
Rotation
   Use the rotation of the object.
Scale
   Use the size of the object.


Group
-----

Dupli Group
   The objects that belong to a group are duplicated sequentially in the place of the particles.

Whole Group
   Use the whole group at once, instead of one of its elements, the group being displayed in place of each particle.
Pick Random
   The objects in the group are selected in a random order, and only one object is displayed in place of a particle.
   Please note that this mechanism fully replaces old Blender particles system using parentage
   and DupliVerts to replace particles with actual geometry.
   This method is fully deprecated and does not work anymore.
Use Count
   Use objects multiple times in the same groups.
   Specify the order and number of times to repeat each object with the list view that appears.
   You can duplicate an object in the list with the :kbd:`Plus` button,
   or remove a duplicate with the :kbd:`Minus` button.

Use Global
   Use object's global coordinates for duplication.
Rotation
   Use the rotation of the objects.
Scale
   Use the size of the objects.
