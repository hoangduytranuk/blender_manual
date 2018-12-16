
********
Geometry
********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Geometry`


Volume Sampling
===============

Step Size
   Distance between volume shader samples when rendering the volume.
   Lower values give more accurate and detailed results but also increased render time.
Max Steps
   Maximum number of steps through the volume before giving up,
   to protect from extremely long render times with big objects or small step sizes.


.. _bpy.types.CyclesRenderSettings.*dicing_rate:
.. _cycles-subdivision-rate:

Subdivision Rate
================

These settings are used to control :doc:`Adaptive Subdivision </render/cycles/settings/objects/adaptive_subsurf>`.

.. note::

   These Options are only available if :ref:`Experimental Feature Set <cycles-experimental-features>` is turned on.

Render
   Size of :term:`micropolygons` in pixels.
Preview
   Size of :term:`micropolygons` in pixels while preview rendering.

.. _bpy.types.CyclesRenderSettings.offscreen_dicing_scale:

Offscreen Scale
   Multiplier for dicing rate of geometry outside of the camera view.
   The dicing rate of objects is gradually increased the further they are outside the camera view.
   Lower values provide higher quality reflections and shadows for off screen objects,
   while higher values use less memory.

.. _bpy.types.CyclesRenderSettings.max_subdivisions:

Max Subdivisions
   Stop subdividing when this level is reached even if the dice rate would produce finer :term:`tessellation`.

.. _bpy.types.CyclesRenderSettings.dicing_camera:

Dicing Camera
   Camera to use as reference point when subdividing geometry,
   useful to avoid crawling artifacts in animations when the scene camera is moving.


.. _cycles-settings-scene-render-geometry:

Hair
====

These are global settings that apply to all instances of hair systems.
The resolution of the strands is controlled by the step values in particle settings.
Each hair system uses the material identified in the particle settings in the same way as Blender Internal.

.. seealso::

   There are also object-level hair settings for each particle system which can be found
   in the :doc:`Hair Settings </render/cycles/settings/objects/hair>`.

Use Hair
   Enables rendering of hair particle systems.

Primitive
   Triangles
      Uses a triangle mesh.

      Resolution
         Number of times to subdivide the hair.
         Higher values gives better quality results at the cost of increased memory usage.
   Line Segments
      Uses a straight curve primitive.
   Curve Segments
      Uses a smooth Cardinal curve primitive. These interpolate a path through the curve keys.
      However, it renders slower than line segments.

      Curve Subdivisions
         The interpolated path is subdivided to give points to connect.
         The parameter subdivisions sets the number of divisions used.

Shape
   Thick
      Cylindrical segments between two points.

      Cull back-faces
         Excludes strands emitted from the mesh backfacing the camera.

   Ribbons
      Are flat planes following the strand direction facing the camera.
Min Pixels
   Strands that are further away will be made wider, which is compensated with transparency to keep the look similar.
   This effect is only applied for camera rays. It works best with ribbon primitives.
