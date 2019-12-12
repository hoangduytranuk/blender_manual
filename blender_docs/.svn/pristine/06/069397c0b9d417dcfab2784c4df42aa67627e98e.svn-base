.. _bpy.types.TransformCacheConstraint:

**************************
Transform Cache Constraint
**************************

The *Transform Cache Constraint* is used to stream animations from
:doc:`Alembic </files/import_export/alembic>` made at the transformation matrix level
(for example rigid bodies, or camera movements).

When :doc:`importing an Alembic file </files/import_export/alembic>`,
Transform Cache constraints are automatically added to objects with animated transforms.
For time-varying meshes (so deforming animations),
the :doc:`Mesh Sequence Cache modifier </modeling/modifiers/modify/mesh_sequence_cache>` is used.


Options
=======

Cache File
   Data-block menu to select the Alembic file.

   File Path
      Path to the Alembic file.

Is Sequence
   Whether or not the cache is separated in a series of files.
Override Frame
   Whether to use a custom frame for looking up data in the cache file,
   instead of using the current scene frame.

   Frame
      The time to use for looking up the data in the cache file,
      or to determine which to use in a file sequence.

Manual Transform Scale
   Value by which to enlarge or shrink the object with respect to the world's origin.
Object Path
   The path to the Alembic object inside the archive.
Vertices/Faces/UV/Color
   Type of data to read for a mesh object respectively:
   vertices, polygons, UV maps and vertex color layers.
