
*********************
Rigid Body Properties
*********************

Rigid Body
==========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Rigid Body`

.. TODO2.8:
   .. figure:: /images/physics_rigid-body_properties_panel.png

      Default rigid body panel.

Type
   Role of the rigid body in the simulation.
   Active objects can be simulated dynamically, passive object remain static.

   Active
      Object is directly controlled by simulation results.
      The possibility to select this type also available with *Add Active*
      button in the Physics tab of the Toolbar.
   Passive
      Object is directly controlled by animation system.
      Thus, this type is not available for `Dynamics`_.
      The possibility to select this type also available with *Add Passive* button
      in the Physics tab of the Toolbar.

Mass
   Specifies how heavy the object is and "weights" irrespective of gravity.
   There are predefined mass preset available with the *Calculate Mass* button
   in the Physics tab of the Toolbar.

   Calculate Mass
      Automatically calculate mass values for rigid body objects based on its volume.
      There are many useful presets available from the menu, listing real-world objects.

      .. note::

         Also you can have *Custom* mass material type,
         which is achieved by setting a custom density value (kg/m\ :sup:`3`).
Dynamic
   Enables/disables rigid body simulation for object.
Animated
   Allows the rigid body additionally to be controlled by the animation system.


Rigid Body Collisions
=====================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Rigid Body --> Collisions`

.. TODO2.8:
   .. figure:: /images/physics_rigid-body_properties_collisions.png

      Rigid Body Collisions panel.


Collision Shapes
----------------

The Shape option determines the collision shape of the object.


.. rubric:: Primitive Shapes

These are best in terms of memory/performance but do not
necessarily reflect the actual shape of the object.
They are calculated based on the object's bounding box.
The center of gravity is always in the middle for now.
Primitive shapes can be shown in the viewport by
enabling *Bounds* in the :menuselection:`Object --> Display` panel.

Box
   Box-like shapes (e.g. cubes), including planes (e.g. ground planes).
   The size per axis is calculated from the bounding box.
Sphere
   Sphere-like shapes. The radius is the largest axis of the bounding box.
Capsule
   This points up the Z axis.
Cylinder
   This points up the Z axis.
   The height is taken from the Z axis, while the radius is the larger of the X or Y axes.
Cone
   This points up the Z axis.
   The height is taken from the Z axis, while the radius is the larger of the X or Y axes.


.. rubric:: Mesh-Based Shapes

These are calculated based on the geometry of the object so they are a better representation of the object.
The center of gravity for these shapes is the object origin.

Convex Hull
   A mesh-like surface encompassing (e.g. shrink-wrap over) all vertices (best results with fewer vertices).
   A convex approximation of the object, has a good performance and stability.
Mesh
   :term:`Mesh` consisting of triangles only, allowing for more detailed interactions than convex hulls.
   Allows to simulate concave objects, but is rather slow and unstable.


Mesh Source
-----------

Users can now specify the mesh *Source* for *Mesh* bases collision shapes:

Base
   The base mesh of the object.
Deform
   Includes any deformations added to the mesh (shape keys, deform modifiers).

   Deforming
      Mesh shapes can deform during simulation.
Final
   Includes all deformations and modifiers.


Surface Response
----------------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Rigid Body --> Surface Response`

Friction
   Resistance of object to movement. Specifies how much velocity is lost when objects collide with each other.
Bounciness
   Tendency of object to bounce after colliding with another (0 to 1) (rigid to perfectly elastic).
   Specifies how much objects can bounce after collisions.

Collision Groups
   Allows rigid body collisions allocate on different groups (maximum 20).


Sensitivity
-----------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Rigid Body --> Sensitivity`

Margin
   Threshold of distance near surface where collisions are still considered (best results when non-zero).

The collision margin is used to improve the performance and stability of rigid bodies.
Depending on the shape, it behaves differently: some shapes embed it,
while others have a visible gap around them.

The margin is *embedded* for these shapes:

- Sphere
- Box
- Capsule
- Cylinder
- Convex Hull: Only allows for uniform scale when embedded.

The margin is *not embedded* for these shapes:

- Cone
- Active Triangle Mesh
- Passive Triangle Mesh: Can be set to 0 most of the time.


Dynamics
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Rigid Body --> Dynamics`

.. TODO2.8:
   .. figure:: /images/physics_rigid-body_properties_dynamics.png

      Rigid Body Dynamics panel.

Used to control the physics of the rigid body simulation.
This panel is available only for *Active* type of rigid bodies.

Damping
   Translation
      Amount of linear velocity that is lost over time.
   Rotation
      Amount of angular velocity that is lost over time.

Deactivation
   Enable Deactivation
      Enable deactivation of resting rigid bodies. Allows object to be deactivated during the simulation
      (improves the performance and stability, but can cause glitches).
   Start Deactivated
      Starts objects deactivated. They are activated on collision with other objects.
   Linear Velocity
      Specifies the linear deactivation velocity below which the rigid body is deactivated and simulation stops
      simulating object.
   Angular Velocity
      Specifies the angular deactivation velocity below which the rigid body is deactivated and simulation stops
      simulating object.

