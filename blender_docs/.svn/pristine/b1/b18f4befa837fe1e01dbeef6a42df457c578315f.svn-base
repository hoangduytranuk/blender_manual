
****************
Viewport Display
****************

.. _bpy.types.FluidDomainSettings.display_thickness:

Thickness
   Factor that scales the thickness of the grid that is currently being displayed.

.. _bpy.types.FluidDomainSettings.display_interpolation:

Interpolation
   Interpolation method to use for the visualization of the fluid grid.

   Linear
      Linear interpolation between voxels. Gives good smoothness and speed.

   Cubic
      Cubic interpolation between voxels. Gives smoothed high quality interpolation, but is slower.

.. _bpy.types.FluidDomainSettings.slice_method:

Slicing
   How to slice the volume for viewport rendering.

   View
      Slice the volume parallel to the view plane.

   Axis
      Slice the volume parallel to the major axis.

.. _bpy.types.FluidDomainSettings.axis_slice_method:

Method
   Full
      Slice the whole domain object.

   Single
      Perform a single slice of the domain object.

      .. _bpy.types.FluidDomainSettings.slice_axis:

      Axis
         Auto
            Adjust slice direction according to the view direction.

         X/Y/Z
            Slice along the X/Y/Z axis.

      .. _bpy.types.FluidDomainSettings.slice_depth:

      Position
         Position of the slice relative to the length of the respective domain side.

.. _bpy.types.FluidDomainSettings.slice_per_voxel:

Slice Per Voxel
   Determines how many slices per voxel should be generated.


.. _bpy.types.FluidDomainSettings.use_color_ramp:

Color Mapping
=============

Use a specific color map for the visualization of the simulation field.
This comes in handy during debugging or when making more advanced
adjustments to the simulation. For instance, if the actual color of
a fire simulation is barely visible in the viewport then changing
the color profile can help to see the real size of the flame.

.. _bpy.types.FluidDomainSettings.coba_field:

Field
   The simulation field used in the display options (e.g. density, fuel, heat).

   .. list-table:: Comparison of a fire simulation with and without color mapping.

      * - .. figure:: /images/physics_fluid_type_domain_gas_viewport-display_colormapping-1.png

             Slice view of "fire" grid without color mapping.

        - .. figure:: /images/physics_fluid_type_domain_gas_viewport-display_colormapping-2.png

             Slice view of "fire" grid with color mapping.


.. _bpy.types.FluidDomainSettings.show_velocity:

Debug Velocity
==============

Visualization options for the velocity field.

.. _bpy.types.FluidDomainSettings.vector_display_type:

Display As
   Streamlines
      Choose to display the velocity vectors as "Streamlines".

   Needle
      Choose to display the velocity vectors as "Needles".

.. _bpy.types.FluidDomainSettings.vector_scale:

Scale
   Scale the velocity vectors by this size in the viewport.
