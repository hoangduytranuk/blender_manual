
*******
Alembic
*******

From the `Alembic home page <https://www.alembic.io/>`__:

   Alembic is an open computer graphics interchange framework. Alembic distills complex, animated
   scenes into a non-procedural, application-independent set of baked geometric results.
   This 'distillation' of scenes into baked geometry is exactly analogous to the distillation of
   lighting and rendering scenes into rendered image data.

   Alembic is focused on efficiently storing the computed results of complex procedural geometric constructions.
   It is very specifically **not** concerned with storing the complex dependency graph
   of procedural tools used to create the computed results.
   For example, Alembic will efficiently store the animated vertex positions and
   animated transforms that result from an arbitrarily complex animation and simulation process
   which could involve enveloping, corrective shapes, volume-preserving simulations,
   cloth and flesh simulations, and so on.
   Alembic will not attempt to store a representation of the network of computations (rigs, basically)
   which are required to produce the final, animated vertex positions and animated transforms.

:abbr:`TL;DR (Too long; didn't read.)`: Alembic can be used to write an animated mesh to disk, and
read it back quickly and efficiently. This means that a mesh can be animated with a very CPU-intensive rig,
'baked' to an Alembic file, and loaded into the shot file for shading and lighting
with only moderate CPU usage.

Support for the Alembic file format was introduced in
`Blender 2.78 <https://wiki.blender.org/wiki/Reference/Release_Notes/2.78>`__.

Due to the Open Source nature of the Alembic standard as well as
the C++ library implementing that standard, **Blender can be used in a hybrid pipeline**.
For example, other software, such as Houdini or Maya, can export files to Alembic,
which can then be loaded, shaded, and rendered in Blender.
It is also possible to animate characters (or other models) in Blender, export to Alembic, and
load those files into other software for further processing.


Exporting to Alembic Files
==========================

This section describes the effect of the different export options.


Manual Transform
----------------

.. figure:: /images/files_import-export_alembic_export-panel-scene-options.png
   :align: right

   Alembic Export options.

Scale
   This sets the global scale of the Alembic file. Keep it at the default value of 1.0 to use
   Blender's units.


Scene Options
-------------

Start Frame and End Frame
   Sets the frame range to export to Alembic. This defaults to the current scene frame range.
Sub-frame Sampling
   These options control the sub-frame sampling of animations.

   Transform Samples
      Transform Samples sets the number of times per frame at which animated transformations
      are sampled and written to Alembic.
   Geometry Samples
      Geometry Samples sets the same, but then for animated geometry.
   Shutter Open/Close
      Shutter Open/Close define the interval [open, close] over which those samples are taken.
      The valid range is -1 to 1, where -1 indicates the previous frame,
      0 indicates the current frame, and 1 indicates the next frame.

      For example, if information for detailed mesh motion blur is desired, some subframes around
      the current frame can be written to Alembic by using a sample count of 5,
      Shutter Open at -0.25 and Shutter Close at 0.25.
      This mimics a "180 degree" shutter, opening 90 degrees before the frame
      and closing 90 degrees after the frame.
Selected Objects Only
   When enabled, exports only the selected objects. When disabled, all objects are exported.
Renderable Objects Only
   This is useful to, for example, avoid exporting custom bone shapes.
Visible Layers Only
   Limits the export to scene layers that are currently visible.
Flatten Hierarchy
   When disabled, parent/child relations between objects are exported too. Any parent object that
   is not exported itself, but with children that *are* exported, is replaced by an Empty.
   When enabled, parent/child relations are not exported, and transformations are all written in
   world coordinates.


Object Options
--------------

.. figure:: /images/files_import-export_alembic_export-panel-object-options.png
   :align: right

   Object options.

UVs
   When enabled, UV maps are exported. Although the Alembic standard only supports a single UV
   map, Blender exports all UV maps in a way that should be readable by other software.
Pack UV Islands
   Generates an optimized UV layout with non-overlapping islands
   that tries to efficiently fill the :term:`Texture Space`.
   See the :ref:`pack islands operator <editors-uv-editing-layout-pack_islands>`
   that works with the same principle for more information.
Normals
   When enabled, an object's :term:`normals <normal>` are exported.
Vertex Colors
   When enabled, exports vertex colors. At this moment, this only supports static vertex colors,
   and not dynamically animated vertex colors.
Face Sets
   Exports the material names per face. The material data is not exported but only material names.
Use Subdivision Schema
   Writes polygonal meshes using the "SubD" Alembic schema, rather than the "PolyMesh" schema.
   This tells the program opening the file to apply its form of a non-destructive subdivision.
Apply Subdivision Surface
   Applies any :doc:`Subdivision surface modifiers </modeling/modifiers/generate/subdivision_surface>`
   before writing to Alembic.
Triangulate
   Triangulates the mesh before writing to Alembic.
   For more detail on the specific option see the
   :doc:`Triangulate Modifier </modeling/modifiers/generate/triangulate>`.


Particle Systems
----------------

.. figure:: /images/files_import-export_alembic_export-panel-particle-systems.png
   :align: right

   Particle Systems options.

Alembic has no support for Particle Systems, in the same way that it does not support armatures.
Hair is exported as animated zero-width curves. Particles are exported as animated points.
