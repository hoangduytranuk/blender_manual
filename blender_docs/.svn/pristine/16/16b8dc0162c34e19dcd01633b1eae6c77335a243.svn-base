.. _bpy.types.SoftBodySettings:

********
Settings
********

Soft Body
=========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body`

Collision Collection
   If set, soft body collides with objects from the collection, instead of using objects that are on the same layer.

Object
   Friction
      The friction of the surrounding medium. Generally friction dampens a movement.
      The larger the friction, the more viscous is the medium.
      Friction always appears when a vertex moves relative to its surround medium.
   Mass
      Mass value for vertices.
      Larger mass slows down acceleration, except for gravity where the motion is constant regardless of mass.
      Larger mass means larger inertia, so also braking a soft body is more difficult.
   Control Point
      You can paint weights and use a specified vertex group for mass values.

Simulation
   Speed
      You can control the internal timing of the soft body system with this value.
      It sets the correlation between frame rate and tempo of the simulation.
      A free falling body should cover a distance of about ten meters after one second.
      You can adjust the scale of your scene and simulation with this correlation. If you
      render with 25 frames per second, you will have to set *Speed* to 1.3.



Soft Body Cache
===============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body --> Cache`

Soft Body physics simulations use a unified system for caching and baking.
See :doc:`Particle Cache </physics/particles/emitter/cache>` and
:doc:`General Baking </physics/baking>` documentation for reference.


.. _physics-softbody-settings-goal:

Soft Body Goal
==============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body --> Goal`

Use Goal
   Enabling this tells Blender to use the motion from animations
   (F-curves, armatures, parents, lattices, etc.) in the simulation.
   The "goal" is the desired end position for vertices based on this animation.

   See :ref:`exterior forces <physics-softbody-forces-exterior-goal>` for details.

Vertex Group
   Use a vertex group to allow per-vertex goal weights (multiplied by the *Default* goal).

Goal Settings
   Stiffness
      The spring stiffness for *Goal*. A low value creates very weak springs
      (more flexible "attachment" to the goal), a high value creates a strong spring
      (a stiffer "attachment" to the goal).
   Damping
      The friction coefficient for *Goal*. Higher values give damping of the spring effect (little jiggle),
      and the movement will soon come to an end.
Goal Strength
   Default
      Goal weight/strength for all vertices when no *Vertex Group* is assigned.
      If you use a vertex group the weight of a vertex defines its goal.
   Minimum/Maximum
      When you use a vertex group, you can use the *Minimum* and *Maximum* to fine-tune (clamp) the weight values.
      The lowest vertex weight will become *Minimum*, the highest value becomes *Maximum*.


.. _physics-softbody-settings-edges:

Soft Body Edges
===============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body --> Edges`

Use Edges
   Allow the edges in a mesh object to act like springs.
   See :doc:`interior forces </physics/soft_body/forces/interior>`.

Springs
   Springs
      Use a specified vertex group for spring strength values.
   Pull
      The spring stiffness for edges (how much the edges are allowed to stretch).
      A low value means very weak springs (a very elastic material),
      a high value is a strong spring (a stiffer material) that resists being pulled apart.

      A value of 0.5 is latex, 0.9 is like a sweater, 0.999 is a highly-starched napkin or leather.
      The soft body simulation tends to get unstable if you use a value of 0.999,
      so you should lower this value a bit if that happens.
   Push
      How much the soft body resists being scrunched together, like a compression spring.
      Low values for fabric, high values for inflated objects and stiff material.
   Damp
      The friction for edge springs. High values (max of 50) dampen the *Push*/*Pull* effect and calm down the cloth.
   Plasticity
      Permanent deformation of the object after a collision.
      The vertices take a new position without applying the modifier.
   Bending
      This option creates virtual connections between a vertex and the vertices connected to its neighbors.
      This includes diagonal edges. Damping also applies to these connections.
   Length
      The edges can shrink or be blown up. This value is given in percent,
      0 disables this function. 100% means no change, the body keeps 100% of his size.

Collision
   Edge
      Checks for edges of the soft body mesh colliding.
   Face
      Checks for any portion of the face of the soft body mesh colliding (computationally intensive!).
      While *Face* enabled is great, and solves lots of collision errors,
      there does not seem to be any dampening settings for it,
      so parts of the soft body object near a collision mesh tend to "jitter" as they bounce off and fall back,
      even when there is no motion of any meshes. Edge collision has dampening, so that can be controlled,
      but Deflection dampening value on a collision object does not seem to affect the face collision.

.. _physics-softbody-settings-aerodynamics:

Aerodynamics
   Force from surrounding media.
   See :ref:`exterior forces <physics-softbody-forces-exterior-aerodynamics>` for details.

   Type
      Simple
         Edges receive a drag force from the surrounding media.
      Lift Force
         Edges receive a lift force when passing through the surrounding media.
   Factor
      How much aerodynamic force to use. Try a value of 30 at first.

Stiff Quads
   Use Stiff Quads
      For quad faces, the diagonal edges are used as springs.
      This stops quad faces to collapse completely on collisions (what they would do otherwise).
   Shear
      Stiffness of the virtual springs created for quad faces.


.. _physics-softbody-settings-self-collision:

Soft Body Self Collision
========================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body --> Self Collision`

.. note::

   *Self-Collision* is working only if you have activated *Use Edges*.

Self Collision
   When enabled, allows you to control how Blender will prevent the soft body from intersecting with itself.
   Every vertex is surrounded with an elastic virtual ball.
   Vertices may not penetrate the balls of other vertices.
   If you want a good result you may have to adjust the size of these balls.
   Normally it works pretty well with the default options.

Calculation Type
   Manual
      The *Ball Size* directly sets the ball size.
   Average
      The average length of all edges attached to the vertex is calculated and then multiplied
      with the *Ball Size* setting. Works well with evenly distributed vertices.
   Minimal/Maximal
      The ball size is as large as the smallest/largest spring length of the vertex multiplied with the *Ball Size*.
   Average Min Max
      Size = ((Min + Max)/2) × *Ball Size*.

Ball Size
   Fraction of the length of attached edges.
   The edge length is computed based on the choosen algorithm.
   This setting is the factor that is multiplied by the spring length.
   It is a spherical distance (radius) within which, if another vertex of the same mesh enters,
   the vertex starts to deflect in order to avoid a self-collision.
   Set this value to the fractional distance between vertices that you want them to have their own "space".
   Too high of a value will include too many vertices all the time and slow down the calculation.
   Too low of a level will let other vertices get too close and thus possibly intersect because
   there will not be enough time to slow them down.
Stiffness
   How elastic that ball of personal space is.
   A high stiffness means that the vertex reacts immediately to another vertex enters their space.
Dampening
   How the vertex reacts.
   A low value just slows down the vertex as it gets too close. A high value repulses it.

Collisions with other objects are set in the (other) :doc:`Collision panel </physics/collision>`.
To collide with another object they have to share at least one common layer.


.. _physics-softbody-settings-solver:

Soft Body Solver
================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Soft Body --> Solver`

The settings in the *Soft Body Solver* panel determine the accuracy of the simulation.

Step Size
   Min Step
      Minimum simulation steps per frame. Increase this value, if the soft body misses fast-moving collision objects.
   Max Step
      Maximum simulation steps per frame.
      Normally the number of simulation steps is set dynamically
      (with the *Error Limit*) but you have probably a good reason to change it.
   Auto-Step
      Use velocities for automatic step sizes.
      Helps the Solver figure out how much work it needs to do based on how fast things are moving.

Error Limit
   Rules the overall quality of the solution delivered. Default 0.1.
   The most critical setting that defines how precise the solver should check for collisions.
   Start with a value that is half the average edge length.
   If there are visible errors, jitter, or over-exaggerated responses, decrease the value.
   The solver keeps track of how "bad" it is doing and the *Error Limit* causes the solver to
   do some "adaptive step sizing".

Diagnostics
   Print Performance to Console
      Prints on the console how the solver is doing.
   Estimate Matrix
      Estimate matrix, split to ``COM``, ``ROT``, ``SCALE``.

.. (TODO) explain what it is, when it can be useful

   Center of mass -- Location of the center of mass.
   Rot Matrix -- Estimated the rotation matrix.
   Scale Matrix -- Estimated the scale matrix.

Helpers
   These settings allow you to control how Blender will react (deform) the soft body
   once it either gets close to or actually intersects (cuts into) another collision object on the same layer.

   Choke
      Calms down (reduces the exit velocity of) a vertex or edge once it penetrates a collision mesh.
   Fuzzy
      Fuzziness while on collision, high values make collision handling faster but less stable.
      Simulation is faster, but less accurate.
