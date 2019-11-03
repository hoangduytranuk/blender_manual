
*************
Data Transfer
*************

The *Data Transfer* tool transfers several types of data from one mesh to another.
Data types include vertex groups, UV maps, vertex colors, custom normals...

Transfer works by generating a mapping between source mesh's items (vertices, edges, etc.)
and destination ones, either on a one-to-one basis, or mapping several source items
to a single destination one by interpolated mapping.


.. _bpy.ops.object.data_transfer:

Data
====

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Relations --> Transfer Mesh Data`

Transfers data layer(s) from active to selected meshes.

Freeze Operator
   Prevent changes to settings to re-run the operator.
   This is useful if you are editing several settings at once with heavy geometry.
Data Type
   Which data to transfer.

   .. figure:: /images/modeling_meshes_editing_data-transfer_menu.png

      Data types.

Create Data
   Add data layers on destination meshes if needed.
Vertex Mapping
   Method used to map source vertices to destination ones.
   Because the options change depending on the *Data Type*
   options are explained in `Vertex Mapping`_ below.


Vertex Mapping
--------------

Topology
^^^^^^^^

The simplest option, expects both meshes to have identical number of items, and match them by order (indices).
Useful e.g. between meshes that were identical copies, and got deformed differently.


One-To-One Mappings
^^^^^^^^^^^^^^^^^^^

Those always select only one source item for each destination one, often based on shortest distance.

Vertices
   Nearest Vertex
      Uses source's nearest vertex.

   Nearest Edge Vertex
      Uses source's nearest vertex of source's nearest edge.

   Nearest Face Vertex
      Uses source's nearest vertex of source's nearest face.

Edges
   Nearest Vertices
      Uses source's edge which vertices are nearest from destination edge's vertices.

   Nearest Edge
      Uses source's nearest edge (using edge's midpoints).
   Nearest Face Edge
      Uses source's nearest edge of source's nearest face (using edge's midpoints).
Face Corners
   A face corner is not a real item by itself, it's some kind of split vertex attached to a specific face.
   Hence both vertex (location) and face (normal, ...) aspects are used to match them together.

   Nearest Corner and Best Matching Normal
      Uses source's corner having the most similar *split* normal with destination one,
      from those sharing the nearest source's vertex.
   Nearest Corner and Best Matching Face Normal
      Uses source's corner having the most similar *face* normal with destination one,
      from those sharing the nearest source's vertex.
   Nearest Corner of Nearest Face
      Uses source's nearest corner of source's nearest face.
Faces
   Nearest Face
      Uses source's nearest face.
   Best Normal-Matching:
      Uses source's face which normal is most similar with destination one.


Interpolated Mappings
^^^^^^^^^^^^^^^^^^^^^

Those use several source items for each destination one, interpolating their data during the transfer.

Vertices
   Nearest Edge Interpolated
      Uses nearest point on nearest source's edge, interpolates data from both source edge's vertices.
   Nearest Face Interpolated
      Uses nearest point on nearest source's face, interpolates data from all that source face's vertices.
   Projected Face Interpolated
      Uses point of face on source hit by projection of destination vertex along its own normal,
      interpolates data from all that source face's vertices.
Edges
   Projected Edge Interpolated
      This is a sampling process. Several rays are cast from along the destination's edge
      (interpolating both edge's vertex normals), and if enough of them hit a source's edge,
      all hit source edges' data are interpolated into destination one.
Face Corners
   A face corner is not a real item by itself, it's some kind of split vertex attached to a specific face.
   Hence both vertex (location) and face (normal, ...) aspects are used to match them together.

   Nearest Face Interpolated
      Uses nearest point of nearest source's face, interpolates data from all that source face's corners.
   Projected Face Interpolated
      Uses point of face on source hit by projection of destination corner along its own normal,
      interpolates data from all that source face's corners.
Faces
   Projected Face Interpolated
      This is a sampling process. Several rays are cast from the whole destination's face (along its own normal),
      and if enough of them hit a source's face, all hit source faces' data are interpolated into destination one.


Further Options
---------------

Auto Transform
   Automatically computes the transformation to get the best possible match between source and destination meshes.

   This allows to match and transfer data between two meshes with similar shape,
   but transformed differently. Note that you'll get best results with exact copies of the same mesh.
   Otherwise, you'll likely get better results
   if you "visually" make them match in 3D space (and use *Object Transform*) instead.
Object Transform
   Evaluate source and destination meshes in global space.
Only Neighbor Geometry
   Source elements must be closer than given distance from destination one.

   Max Distance
      Maximum allowed distance between source and destination element (for non-topology mappings).

.. (TODO) The below definition is confusing for users. Change?

Ray Radius
   Width of rays. Useful when ray casting against vertices or edges.
Mix Mode
   How to affect destination elements with source values.

   All
      Replaces everything in destination (note that *Mix Factor* is still used).
   Above Threshold
      Only replaces destination value if it is above given threshold *Mix Factor*.
      How that threshold is interpreted depends on data type,
      note that for boolean values this option fakes a logical AND.
   Below Threshold
      Only replaces destination value if it is below given threshold *Mix Factor*.
      How that threshold is interpreted depends on data type,
      note that for boolean values this option fakes a logical OR.
   Mix, Add, Subtract, Multiply
      Apply that operation, using mix factor to control how much of source or destination value to use.
      Only available for a few types (vertex groups, vertex colors).
Mix Factor
   How much of the transferred data gets mixed into existing one (not supported by all data types).


.. _bpy.ops.object.datalayout_transfer:

Data Layout
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Relations --> Transfer Mesh Data Layout`

Transfers layout of data layer(s) from active to selected meshes.

Data Type
   Which data to transfer.

   .. figure:: /images/modeling_meshes_editing_data-transfer_menu.png

      Data types.

Exact Match
   Also Delete some data layers from destination if necessary, so that it matches the source exactly.
Source Layers Selection
   Which layers to transfer, in case of multi-layer types.

   Active Layer
      Only transfer the active data layer.
   All Layers
      Transfer all data layers.

Destination Layers Matching
   How to match source and destination layers.

   By Name
      Match target data layers to affect by name.
   By Order
      Match target data layers to affect by order (indices).

.. seealso::

   :doc:`Data Transfer Modifier </modeling/modifiers/modify/data_transfer>`
