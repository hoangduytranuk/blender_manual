
****************************
Mesh Sequence Cache Modifier
****************************

The Mesh Sequence Cache modifier loads data from :doc:`Alembic </files/import_export/alembic>` files.
It supports static meshes, but is mostly used to load animated meshes.
Despite its name, this modifier also supports curves. It also handles file sequences,
as well as meshes and curves with varying topology (like the result of fluid simulations).

When :doc:`importing an Alembic file </files/import_export/alembic>`,
Mesh Sequence Cache modifiers are automatically added to time-varying meshes.
For time-varying object transforms (so animation of rotation, location, or scale),
the :ref:`Transform Cache Constraint <bpy.types.TransformCacheConstraint>` is used.

Non-Alembic files, like MDD and PC2 files, can be loaded using
the :doc:`Mesh Cache modifier </modeling/modifiers/modify/mesh_cache>`.


Options
=======

Cache File
   Data-block menu to select the Alembic file.

   File Path
      Path to Alembic file.
Is sequence
   Whether or not the cache is separated in a series of files.
Override Frame
   Whether to use a custom frame for looking up data in the cache file,
   instead of using the current scene frame.

   Frame
      The time to use for looking up the data in the cache file,
      or to determine which to use in a file sequence.
Manual Transform Scale
   Value by which to enlarge or shrink the object with respect to the world's origin.
   (Only applicable through
   a :doc:`Transform Cache Constraint </animation/constraints/transform/transform_cache>`.)
Object Path
   The path to the Alembic object inside the archive.

Read Data
   Type of data to read for a mesh object, respectively: vertices,
   polygons, UV maps and Vertex Color layers.

   Vertices, Faces, UV, Color
