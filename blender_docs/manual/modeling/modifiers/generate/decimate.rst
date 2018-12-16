.. _bpy.types.DecimateModifier:

*****************
Decimate Modifier
*****************

The Decimate Modifier allows you to reduce the vertex/face count of a mesh with minimal shape changes.

This is not usually used on meshes which have been created by modeling carefully and economically
(where all vertices and faces are necessary to correctly define the shape).
But if the mesh is the result of complex modeling,
sculpting and/or applied Subdivision Surface/Multiresolution Modifiers,
the Decimate Modifier can be used to reduce the polygon count for a performance increase,
or simply remove unnecessary vertices and edges.

The Decimate Modifier is a quick and easy way of reducing the polygon count of
a mesh non-destructively. This modifier demonstrates the advantages of a mesh modifier system
because it shows how an operation which is normally permanent and destroys original mesh data,
can be done interactively and safely using a modifier.

Unlike the majority of existing modifiers, the Decimate Modifier does not allow
you to visualize your changes in Edit Mode.


Options
=======

Decimate Type
-------------

Collapse
^^^^^^^^

.. figure:: /images/modeling_modifiers_generate_decimate_panel-collapse.png

   Decimate Modifier.

Merge vertices together progressively, taking the shape of the mesh into account.

Ratio
   The ratio of faces to keep after decimation.

   - On 1.0: the mesh is unchanged.
   - On 0.5: edges have been collapsed such that half the number of faces remain (see note below).
   - On 0.0: all faces have been removed.

   .. note::

      Although the *Ratio* is directly proportional to the number of remaining faces,
      triangles are used when calculating the ratio.

      This means that if your mesh contains quads, the number of remaining faces will be larger than expected,
      because quads remain unchanged if their edges are not collapsed.

      This is only true if the *Triangulate* option is disabled.

Vertex Group
   A vertex group that controls what parts of the mesh are reduced.

   Factor
      The amount of influence the *Vertex Group* has on the decimation.
Triangulate
   Keeps any resulting triangulated geometry from the decimation process.
Symmetry
   Maintains symmetry on a single axis.


Un-Subdivide
^^^^^^^^^^^^

.. figure:: /images/modeling_modifiers_generate_decimate_panel-un-subdivide.png

   Decimate Modifier.

Can be thought of as the reverse of subdivide.
Attempts to remove edges that were the result of a subdivide operation.
For meshes with a mainly grid-based topology (without giving uneven geometry).
If additional editing has been done after the subdivide operation, the results may be unexpected.

Iterations
   The number of times to perform the un-subdivide operation.
   Two iterations is the same as one subdivide operation, so you will usually want to use even numbers.


Planar
^^^^^^

.. figure:: /images/modeling_modifiers_generate_decimate_panel-planar.png

   Decimate Modifier.

Reduces detail on forms comprised of mainly flat surfaces.

Angle Limit
   Dissolve geometry which form angles lower than this setting.

All Boundaries
   When enabled, all vertices along the boundaries of faces are dissolved.
   This can give nicer results when using a high *Angle Limit*.

Delimit
   Prevent dissolving geometry in certain places.

   Normal
      Does not dissolve edges on the borders of areas where the face normals are reversed.
   Material
      Does not dissolve edges on the borders of where different materials are assigned.
   Seam
      Does not dissolve edges marked as seams.


Further Options
---------------

Face Count
   This label shows the number of remaining faces as a result of applying the Decimate Modifier.
