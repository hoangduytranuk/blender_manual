.. _bpy.types.FluidDomainSettings.domain_type:
.. _bpy.types.FluidDomainSettings.resolution_max:
.. _bpy.types.FluidDomainSettings.time_scale:
.. _bpy.types.FluidDomainSettings.cfl_condition:
.. _bpy.types.FluidDomainSettings.use_adaptive_timesteps:
.. _bpy.types.FluidDomainSettings.timesteps_max:
.. _bpy.types.FluidDomainSettings.timesteps_min:
.. _bpy.types.FluidDomainSettings.gravity:

********
Settings
********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Settings`
   :Type:      Domain

The domain object contains the entire simulation. Fluid simulations cannot leave the domain,
it will either collide with the edge or disappear, depending on the domain's settings.

Keep in mind that large domains need higher resolutions and longer bake times.
You will want to make it just large enough that the simulation will fit inside it,
but not so large that it takes too long to compute the simulation.

To create a domain, add a cube and transform it until it encloses the area where you want
the simulation to take place. Translation, rotation, and scaling are all allowed.
To turn it into a fluid domain, click *Fluid* in the :menuselection:`Properties --> Physics` tab,
then select *Domain* as the fluid *Type*.

.. note::

   You *can* use other shapes of mesh objects as domain objects,
   but the fluid simulator will use the shape's :term:`bounding box` as the domain bounds.
   In other words, the actual shape of the domain will still be rectangular.

Domain Type
   A fluid domain can control either liquid or gas flows. Liquid domains take all liquid flow
   objects that intersect with the domain into consideration. Gas domains consider all
   intersecting *Smoke*, *Fire*, and *Smoke + Fire* flow objects. It is not possible to change
   the domain type dynamically.

Resolution Divisions
   The fluid domain is subdivided into many "cells" called :term:`voxels <voxel>`
   which make up "pixels" of fluid. This setting controls the number of subdivisions in the domain.
   Higher numbers of subdivisions are one way of creating higher resolution fluids.

   Since the resolution is defined in terms of "subdivisions",
   larger domains will need more divisions to get an equivalent resolution to a small domain.
   To help with this, the *Resolution Divisions* can be previewed with a small cube
   shown in the 3D Viewport, to show the size of these divisions.

Time Scale
   Controls the speed of the simulation. Low values result in a "slow motion" simulation,
   while higher values can be used to advance the simulation faster
   (useful for generating fluids for use in still renders).

CFL Number
   Determines the maximum velocity per grid cell and is measured in grid cells per time step.
   Fluid is only allowed to move up to this velocity in one time step. If this threshold is
   exceeded the solver will subdivide the simulation step.

   In general, greater CFL (Courant–Friedrichs–Lewy) numbers will minimize the number of simulation steps
   and the computation time. Yet it will yield less physically accurate behavior for fast fluid flows.
   Smaller CFL numbers result in more simulation steps per frame, longer simulation times
   but more accurate behavior at high velocities (e.g. fast fluid flow colliding
   with obstacle).

Use Adaptive Time Steps
   Lets the solver automatically decide when to perform multiple simulation steps per frame.
   It takes into account the maximum and minimum number of time steps,
   the current *Frame Rate*, and the *Time Scale*.

   Timesteps Maximum
      Maximum number of allowed time steps per frame. If needed, the solver will divide
      a simulation step up to this number of substeps.

   Timesteps Minimum
      Minimum number of allowed time steps per frame. The solver will always perform at least
      this number of simulation steps per frame.

Gravity
   By default the fluid solver will use the global scene gravity. This behavior can be disabled
   in the scene settings. Disabling the global gravity will enable the fluid gravity options.


.. _bpy.types.FluidDomainSettings.use_collision_border_front:
.. _bpy.types.FluidDomainSettings.use_collision_border_back:
.. _bpy.types.FluidDomainSettings.use_collision_border_right:
.. _bpy.types.FluidDomainSettings.use_collision_border_left:
.. _bpy.types.FluidDomainSettings.use_collision_border_top:
.. _bpy.types.FluidDomainSettings.use_collision_border_bottom:

Border Collisions
=================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Settings --> Border Collisions`
   :Type:      Domain (Gas)

Controls which sides of the domain will allow fluid to "pass through" the domain,
making it disappear without influencing the rest of the simulation,
and which sides will deflect fluids.


.. _bpy.types.FluidDomainSettings.alpha:
.. _bpy.types.FluidDomainSettings.beta:
.. _bpy.types.FluidDomainSettings.vorticity:

Smoke
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Settings --> Smoke`
   :Type:      Domain (Gas)

Buoyancy Density
   Buoyant force based on smoke density.

   - Values above 0 will cause the smoke to rise (simulating smoke which is lighter than ambient air).
   - Values below 0 will cause smoke to sink (simulating smoke which is heavier than ambient air).

.. _smoke-domain-heat:

Buoyancy Heat
   Controls how much smoke is affected by temperature.
   The effect this setting has on smoke depends on the per flow object
   :ref:`Initial Temperature <physics-fluid-flow-init-temp>`:

   - Values above 0 will result in the smoke rising when the flow object *Initial Temperature* is
     set to a positive value, and smoke sinking when the flow object *Initial Temperature* is
     set to a negative value.
   - Values below 0 will result in the opposite of positive values,
     i.e. smoke emitted from flow objects with a positive *Initial Temperature* will sink,
     and smoke from flow objects with a negative *Initial Temperature* will rise.

   Note that smoke from multiple flow objects with different temperatures
   will mix and warm up/cool down until an equilibrium is reached.

Vorticity
   Controls the amount of turbulence in the smoke. Higher values will make lots of small swirls,
   while lower values make smoother shapes.

   .. figure:: /images/physics_smoke_types_domain_vorticity.jpg
      :align: center

      Comparison of different amounts of vorticity. The domain on the left has a vorticity of 3,
      while the domain on the right has a vorticity of 0.01.


.. _bpy.types.FluidDomainSettings.use_dissolve_smoke:
.. _bpy.types.FluidDomainSettings.dissolve_speed:
.. _bpy.types.FluidDomainSettings.use_dissolve_smoke_log:

Dissolve
--------

Allow smoke to dissipate over time.

Time
   Speed of smoke's dissipation in frames.
Slow
   Dissolve smoke in a logarithmic fashion. Dissolves quickly at first, but lingers longer.


.. _bpy.types.FluidDomainSettings.burning_rate:
.. _bpy.types.FluidDomainSettings.flame_smoke:
.. _bpy.types.FluidDomainSettings.flame_vorticity:
.. _bpy.types.FluidDomainSettings.flame_max_temp:
.. _bpy.types.FluidDomainSettings.flame_ignition:
.. _bpy.types.FluidDomainSettings.flame_smoke_color:

Fire
====

.. admonition:: Reference
   :class: refbox

   :Type:      Domain
   :Panel:     :menuselection:`Physics --> Fluid --> Settings --> Fire`

Reaction Speed
   How fast fuel burns. Larger values result in smaller flames (fuel burns before it can go very far),
   smaller values result in larger flames (fuel has time to flow farther before being fully consumed).
Flame Smoke
   Amount of extra smoke created automatically to simulate burnt fuel.
Vorticity
   Extra vorticity for flames.
Temperature Maximum
   Maximum temperature of flames. Larger values result in faster rising flames.
Minimum
   Minimum temperature of flames.
Flame Color
   Color of flame created by burnt fuel.


.. _bpy.types.FluidDomainSettings.use_flip_particles:
.. _bpy.types.FluidDomainSettings.simulation_method:
.. _bpy.types.FluidDomainSettings.flip_ratio:
.. _bpy.types.FluidDomainSettings.particle_radius:
.. _bpy.types.FluidDomainSettings.particle_max:
.. _bpy.types.FluidDomainSettings.particle_min:
.. _bpy.types.FluidDomainSettings.particle_number:
.. _bpy.types.FluidDomainSettings.particle_randomness:
.. _bpy.types.FluidDomainSettings.use_fractions:
.. _bpy.types.FluidDomainSettings.fractions_threshold:

Liquid
======

.. admonition:: Reference
   :class: refbox

   :Type:      Domain
   :Panel:     :menuselection:`Physics --> Fluid --> Settings --> Liquid`

Liquid settings control the behavior of the particles which the simulation consists of.
Enabling the liquid checkbox will automatically create a particle system for the simulation.
This particle system visualizes the flow of the simulation. Visualizing the liquid particles is optional.
The fluid simulation will make use of all the fields without an attached particle system too.

.. note::

   Disabling the liquid checkbox will delete the attached particle system and its settings.

Simulation Method
   Determines the particle simulation method. Currently, FLIP is the only option to choose from.

FLIP Ratio
   How much FLIP velocity to use when updating liquid particle velocities. A value of 1.0
   will result in a completely FLIP based simulation. Completely FLIP based simulations
   produce more chaotic splashes and are preferable when simulating greater quantities of liquid.
   When using smaller values the behavior will be less turbulent and splashes are more subtle.
   This is optimal when simulating scenes where the liquid is supposed to be on a small scale.

Particle Radius
   The radius of one liquid particle in grid cells units. This value describes how much area is covered
   by a particle and thus determines how much area around it can be considered as liquid.
   A greater radius will let particles cover more area. This will result in more grids cell being tagged
   as liquid instead of just being empty.

   Whenever the simulation appears to leak or gain volume in an undesired, non physically accurate way it is
   a good idea to adjust this value. That is, when liquid seems to disappear this value needs to be increased.
   The inverse applies when too much liquid is being produced.

Particles Maximum
   The maximum number of liquid particles per grid cell. During a simulation the number of liquid
   particles in a cell can fluctuate: Particles can flow into other cells or can get deleted
   if they move outside the narrow band. Resampling will add new particles considering this maximum.

   This value sets the upper threshold of particles per cell. It is also a good way to estimate how
   many particles there can be in your simulation (one needs to take grid resolution into account too).
   This can be useful before baking and when planning a simulation.

Particles Minimum
   The minimum number of liquid particles per grid cell. Similarly to the maximum particle threshold,
   this value ensures that there are at least a certain amount of particles per cell.

Particle Sampling
   Factor that is used when sampling particles. A higher value will sample more particles.
   Note that particle resampling occurs at every simulation step.

Narrow Band Width
   Controls the width in grid cell units of the narrow band that liquid particles are allowed to flow in.
   A high value will result in a thicker band and can result in an inflow region completely filled
   with particles. Unless the goal of the simulation is to visualize the liquid particles it is
   recommended to not increase the band width significantly as more particles slow down the simulation.

   In some situations increasing this value can help create volume when the simulation appears to leak.
   In all other cases it is best to keep the narrow band as thin as possible since the liquid surface
   contains most details and simulating particles inside the liquid is not an optimal use of computing resources.

Particle Randomness
   New particles are sampled with some randomness attached to their position. This field
   controls this randomness. Higher values will sample the liquid particles more randomly in
   inflow regions. With a value of 0.0 all new particles will be sampled uniformly inside
   their corresponding grid cells.

   When trying to create laminar inflows (little randomness) or more turbulent flows
   (greater randomness) this value can be useful.

Fractional Obstacles
   Enables finer resolution in fluid / obstacle regions (second order obstacles).
   This option reduces the "stepping effect" that results when an obstacles lies inclined inside the domain.
   It also makes liquid flow more smoothly over an obstacle.

Obstacle-Fluid Threshold
   Value to control the smoothness of the fractional obstacle option. Smaller value reduce
   the "stepping effect" but may result particles sticking to the obstacle.
