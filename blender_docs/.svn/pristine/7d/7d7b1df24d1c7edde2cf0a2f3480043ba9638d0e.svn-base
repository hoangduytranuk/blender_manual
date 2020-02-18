
****
Flow
****

Fluid *Flow* types are used to add or remove fluid to a domain object.
Flow objects should be contained within the domain's :term:`bounding box` in order to work.

To define any mesh object as a *Flow* object, add Fluid physics by clicking *Fluid*
in the :menuselection:`Properties --> Physics` tab. Then select *Flow* as the fluid *Type*.
Now you should have a default fluid flow source object.


.. _bpy.types.FluidFlowSettings:

Settings
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Settings`
   :Type:      Flow

Flow Type
   Smoke
      Emit only smoke.
   Fire + Smoke
      Emit both fire and smoke.
   Fire
      Emit only fire. Note that the domain will automatically create some smoke to simulate smoke left by burnt fuel.
   Liquid
      Emit liquid.

Flow Behavior
   Controls if the Flow object either adds (*Inflow*), removes (*Outflow*),
   or turn the mesh itself into fluid (*Geometry*).

   Inflow
      This object will emit fluid into the simulation, like a water tap or base of a fire.

      Use Inflow
         Enables or disables the flow of fluid, this property is useful for animations
         to selectively enable and disable when fluid is being added to the domain.
   Outflow
      Any fluid that enters the :term:`bounding box` of this object will be removed from
      the domain (think of a drain or a black hole). This can be useful in combination with
      an inflow to prevent the whole domain from filling up. Outflow objects can be animated
      and the area where the fluid disappears will follow the object as it moves around.
   Geometry
      All regions of this object that are inside the domain bounding box will be used as
      actual fluid in the simulation. You can place more than one fluid object inside the domain.
      Also make sure that the surface normals are pointing outwards or else they will not simulate properly.
      In contrast to domain objects, the actual mesh geometry is used for fluid objects.

Sampling Substeps
   Number of subframes used to reduce gaps in emission of smoke from fast-moving sources.

   .. figure:: /images/physics_smoke_types_flow-object_subframes.jpg

      Example showing two fast-moving sources.
      The object on the left uses 0 subframes, while the one on the right uses 6.

Smoke Color
   The color of emitted smoke. When smoke of different colors are mixed they will blend together,
   eventually settling into a new combined color.

   .. figure:: /images/physics_smoke_types_flow-object_color-blending.jpg

      Color blending example.

Absolute Density
   Maximum density of smoke allowed within range of the source.

.. _physics-fluid-flow-init-temp:

Initial Temperature
   Difference between the temperature of emitted smoke and the domain's ambient temperature.
   This setting's effect on smoke depends on the domain's :ref:`Initial Temperature <smoke-domain-heat>`.

Density
   Amount of smoke to emit at once.

Fuel
   Amount of "fuel" being burned per second. Larger values result in larger flames,
   smaller values result in smaller flames:

   .. figure:: /images/physics_smoke_types_flow-object_flame-rate.jpg

      Example showing two fire sources.
      The object on the left has a *Flame Rate* of 5, while the one on the right has 0.3.

Vertex Group
   When set, use the specified :doc:`Vertex Group </modeling/meshes/properties/vertex_groups/vertex_groups>`
   to control where smoke is emitted.


.. _bpy.types.FluidFlowSettings.flow_source:
.. _bpy.types.FluidFlowSettings.use_plane_init:
.. _bpy.types.FluidFlowSettings.surface_distance:
.. _bpy.types.FluidFlowSettings.volume_density:
.. _bpy.types.FluidFlowSettings.particle_system:
.. _bpy.types.FluidFlowSettings.use_particle_size:
.. _bpy.types.FluidFlowSettings.particle_size:

Flow Source
-----------

Flow Source
   This setting defines the method used to emit fluid.

   Mesh
      Emit smoke/fire directly from the object's mesh.

      Is Planar
         Defines the effector as either a single dimension object i.e. a plane or the mesh is :term:`non-manifold`.
         This ensures that the fluid simulator will give the most accurate results for these types of meshes.
      Surface Emission
         Maximum distance in :term:`voxels <voxel>` from the surface of the mesh in which fluid is emitted.
         Since this setting uses voxels to determine the distance,
         results will vary depending on the domain's resolution.
      Volume Emission
         Amount of fluid to emit inside the emitter mesh, where 0 is none and 1 is the full amount.
         Note that emitting fluid based on volume may have unpredictable results
         if your mesh is :term:`non-manifold`.

   Particle System :guilabel:`Fire or Smoke Only`:
      Emit smoke/fire from a particle system on the flow object.
      Note that only *Emitter* type particle systems can add smoke.
      See :doc:`Particles </physics/particles/introduction>` for information on how to create a particle system.

      With this option selected, there is a box to select a particle system and one additional setting, *Set Size*.

         Set Size
            When this setting is enabled, it allows the *Size* setting to define
            the maximum distance in voxels at which particles can emit smoke,
            similar to the *Surface Emission* setting for mesh sources.

            When disabled, particles will fill the nearest :term:`voxel` with smoke.


.. _bpy.types.FluidFlowSettings.use_initial_velocity:
.. _bpy.types.FluidFlowSettings.velocity:

Initial Velocity
----------------

When enabled, the fluid will inherit the momentum of the flow source.

Source
   Factor for the inherited velocity. A value of 1 will emit fluid moving at the same speed as the source.
Normal
   When using a *Geometry Flow Source*,
   this option controls how much velocity fluid is given along the source's :term:`normal`.
Initial X, Y, Z
   Controls how much velocity is given in a particular axis.


.. _bpy.types.FluidFlowSettings.use_texture:
.. _bpy.types.FluidFlowSettings.noise_texture:
.. _bpy.types.FluidFlowSettings.texture:

Texture
-------

.. admonition:: Reference
   :class: refbox

   :Type:      Flow
   :Panel:     :menuselection:`Physics --> Fluid --> Settings --> Texture`

When enabled, use the specified texture and settings to control where on
the mesh smoke or fire can be emitted from. These settings have no effect on *Outflow Flow Behavior*.

Texture
   A :ref:`ui-data-id` selector to choose the :doc:`Texture </render/materials/legacy_textures/index>`.
Mapping
   Controls whether to use :ref:`Generated UVs <properties-texture-space>` or manual UV mapping.
Size
   Overall texture scale.
Offset
   Translates the texture along the Z axis.

.. figure:: /images/physics_smoke_types_flow-object_texture-usecase.jpg
   :align: center

   Example of using a texture to control smoke flow.
