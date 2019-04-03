.... _bpy.types.PointDensityTexture:

*********************
Point Density Texture
*********************

Point density renders a given point cloud (object vertices or particle system) as a 3D volume,
using a user-defined radius for the points. Internally,
the system uses a BVH data structure for fast range lookups.

The rendered points are spherical by default, with various smooth falloff options,
as well as simple Turbulence options for displacing the result with noise, adding fine detail.
When using Point Density with a particle system,
additional particle info such as particle velocity, age, and speed,
can be visualized using a color/alpha ramp gradient.


Options
=======

.. figure:: /images/render_blender-render_textures_types_volume_point-density_panel.png

   Point Density panel.

Point Data
   Particle System
      Particle System, Generate point density from a particle system.
   Object Vertices
      Object Vertices, Generate point density from an object's vertices.

Object
   Object to take the point data from.
Radius
   Radius of the points.

   System
      Particle system to use.

Falloff
   Standard
      ..
   Smooth
      ..
   Soft
      ..
   Softness
      ..
   Constant
      Density is constant within the look-up radius.
   Root
      ..
   Particle Age
      ..
   Particle Velocity
      ..
   Velocity Scale
      ..

Falloff Curve
   Use a custom falloff.

Cache
   Coordinate system to cache particles in.

   Global Space
      ..
   Emit Object Space
      ..
   Emit Object Location
      ..

Color Source
   Data to derive the color results from.

   Constant
      Constant color
   Particle Color Sources
      Particle Age
         Lifetime mapped as 0.0 - 1.0 intensity.
      Particle Speed
         Particle speed (absolute magnitude of velocity) mapped as 0.0 - 1.0 intensity.
         An additional color ramp can be used to convert intensity to RGB colors.

         Scale
            Multiplier to bring particle speed within an acceptable range.
      Particle Velocity
         XYZ velocity mapped to RGB colors.

         Scale
            Multiplier to bring particle speed within an acceptable range.
   Vertex Color Sources
      Vertex Color
         Use a vertex color layer for coloring the point density texture.

         .. note::

            Vertex colors are defined per face corner.
            A single vertex can have as many different colors as faces it is part of.
            The actual color of the point density texture is averaged from all vertex corners.

      Vertex Weight
         Use weights from a vertex group as intensity values.
         An additional color ramp can be used to convert intensity to RGB colors.
      Vertex Normals
         Use object-space vertex normals as RGB values.


Turbulence
----------

.. figure:: /images/render_blender-render_textures_types_volume_point-density_turbulence.png

   Turbulence panel.

Adds directed noise to the density at render time.

Influence
   Method for driving added turbulent noise.

   Static
      Noise patterns will remain unchanged, faster and suitable for stills.
   Particle Velocity
      Turbulent noise driven by particle velocity.
   Particle Age
      Turbulent noise driven by the particle's age between birth and death.
   Global Time
      Turbulent noise driven by the global current frame.

Noise Basis
   See :doc:`Here </editors/uv_image/uv/textures/types/procedural/introduction>`.

Size
   Scale of the turbulent noise.
Depth
   Level of detail in the added turbulent noise.
Turbulence Strength
   Strength of the added turbulent noise.
