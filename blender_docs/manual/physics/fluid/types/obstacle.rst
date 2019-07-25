.. _bpy.types.ObstacleFluidSettings:

**************
Fluid Obstacle
**************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid`
   :Type:      Obstacle

This object will be used as an obstacle in the simulation. As with a fluid object,
obstacle objects currently should not intersect. As for fluid objects,
the actual mesh geometry is used for obstacles. For objects with a volume,
make sure that the normals of the obstacle are calculated correctly, and radiating properly
(use the :menuselection:`Mesh --> Normals --> Recalculate Outside` in mesh edit mode),
particularly when using a spinned container.
Applying a :doc:`Subdivision Surface Modifier </modeling/modifiers/generate/subdivision_surface>`
before baking the simulation could also be a good idea if the mesh is not animated.


Options
=======

Volume Initialization Type
   See :ref:`Volume Initialization Type <fluid-initialization>`.

Slip type
   Determines the stickiness of the obstacle surface, called "Surface Adhesion".
   Surface Adhesion depends in the real world on the fluid and the graininess or
   friction/adhesion/absorption qualities of the surface.

   No Slip
      Causes the fluid to stick to the obstacle (zero velocity).
   Free Slip
      Allows movement along the obstacle (only zero normal velocity).
   Partial Slip
      Mixes both types, with 0 being mostly no slip, and 1 being identical to free slip.

   Note that if the mesh is moving, it will be treated as no slip automatically.

.. figure:: /images/physics_fluid_types_obstacle_bndtcomp.jpg

   Example of the different boundary types for a drop falling onto the slanted wall.
   From left to right: no slip, partial slip 0.3, partial slip 0.7 and free slip.

Animated Mesh/Export
   See :ref:`Animated Mesh/Export <fluid-animated-mesh>`.

Amount
   Amount of mixing between no- and free-slip, described above.

Impact Factor
   Amount of fluid volume correction for gain/loss from impacting with moving objects.
   If this object is not moving, this setting has no effect.
   However, if it is and the fluid collides with it, a negative value takes volume away from the Domain,
   and a positive number adds to it. Ranges from -2.0 to 10.0.
