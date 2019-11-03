
**********
Edge Tools
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge`
   :Hotkey:    :kbd:`Ctrl-E`


New Edge/Face from Vertices
===========================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Vertex --> New Edge/Face from Vertices`
   :Hotkey:    :kbd:`F`

It will create an edge or some faces, depending on your selection.

See also :doc:`Creating Geometry </modeling/meshes/editing/basics/make_face_edge>`.


Set Edge Attributes
===================

Edges can have several different attributes that affect how certain other tools affect the mesh.


.. _bpy.ops.mesh.mark_seam:

Mark Seam and Clear Seam
------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Mark Seam/Clear Seam`

Seams are a way to create separations, "islands", in UV maps.
See the :ref:`UV Mapping section <editors-uv-index>` for more details.
These operators set or unset this flag for selected edges.


.. _bpy.ops.mesh.mark_sharp:

Mark Sharp and Clear Sharp
--------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Mark Sharp/Clear Sharp`

The *Sharp* flag is used by the :ref:`split normals <auto-smooth>`
and the :doc:`Edge Split </modeling/modifiers/generate/edge_split>` modifier,
which are part of the smoothing/customized shading techniques.
As seams, it is a property of edges, and these operators set or unset it for selected ones.


.. _modeling-edges-bevel-weight:
.. _bpy.ops.transform.edge_bevelweight:

Adjust Bevel Weight
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Edge Bevel Weight`
               :menuselection:`Sidebar region --> Transform --> Edge Bevel Weight`

This edge property, a value between (0.0 to 1.0),
is used by the :doc:`Bevel Modifier </modeling/modifiers/generate/bevel>`
to control the bevel intensity of the edges.
This operator enters an interactive mode (a bit like transform tools),
where by moving the mouse (or typing a value with the keyboard)
you can set the bevel weight of selected edges. If two or more edges are selected,
this operator alters the average weight of the edges.

.. seealso::

   Vertices also have a bevel weight which can be edited.

   .. TODO2.8 there are no docs for this yet.


.. _modeling-edges-crease-subdivision:
.. _bpy.ops.transform.edge_crease:

Edge Crease
-----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Edge Crease`
               :menuselection:`Sidebar region --> Transform --> Edge Crease`
   :Hotkey:    :kbd:`Shift-E`

This edge property, a value between (0.0 to 1.0), is used by
the :doc:`Subdivision Surface Modifier </modeling/modifiers/generate/subdivision_surface>`
to control the sharpness of the edges in the subdivided mesh.
This operator enters an interactive mode (a bit like transform tools),
where by moving the mouse (or typing a value with the keyboard) you can set the (average)
crease value of selected edges.
A negative value will subtract from the actual crease value, if present.
To clear the crease edge property, enter a value of -1.


.. _bpy.ops.transform.edge_slide:
.. _modeling-meshes-editing-edge-slide:
.. _tool-mesh-edge_slide:

Edge Slide
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Edge Slide`

Slides one or more edges across adjacent faces with a few restrictions involving the selection
of edges (i.e. the selection *must* define a valid loop, see below).

Even :kbd:`E`
   Forces the edge loop to match the shape of the adjacent edge loop.
   You can flip to the opposite vertex using :kbd:`F`. Use :kbd:`Alt-Wheel` to change the control edge.
Flipped :kbd:`F`
   When Even mode is active, this flips between the two adjacent edge loops the active edge loop will match.
Clamp :kbd:`Alt` or :kbd:`C`
   Toggle clamping the slide within the edge extents.
Factor
   Determines the amount of slide performed.
   Negative values correspond to slides toward one face, while positive ones, refer to the other one.
   It is also displayed in the 3D View footer.
Mirror Editing
   Lets you propagate the operation to the symmetrical elements of the mesh (if present, in local X direction).
Correct UVs
   Corrects the corresponding UV coordinates, if these exist, to avoid image distortions.


Usage
-----

By default, the position of vertices on the edge loop move as a percentage of the distance
between their original position and the adjacent edge loop, regardless of the edges' lengths.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_edge-slide-before.png
          :width: 320px

          Selected edge loop.

     - .. figure:: /images/modeling_meshes_editing_edges_edge-slide-after.png
          :width: 320px

          Repositioned edge loop.


Even Mode
^^^^^^^^^

*Even* mode keeps the shape of the selected edge loop the same as one of the edge loops adjacent to it,
rather than sliding a percentage along each perpendicular edge.

In *Even* mode, the tool shows the position along the length of the currently selected edge
which is marked in yellow, from the vertex that has an enlarged red marker.
Movement of the sliding edge loop is restricted to this length. As you move the mouse
the length indicator in the header changes showing where along the length of the edge you are.

To change the control edge that determines the position of the edge loop,
use the :kbd:`Alt-Wheel` to scroll to a different edge.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_edge-slide-even.png
          :width: 320px

          Even Mode enabled.

     - .. figure:: /images/modeling_meshes_editing_edges_edge-slide-even-flip.png
          :width: 320px

          Even Mode with Flip enabled.

Moving the mouse moves the selected edge loop towards or away from the start vertex,
but the loop line will only move as far as the length of the currently selected edge,
conforming to the shape of one of the bounding edge loops.


Limitations & Workarounds
^^^^^^^^^^^^^^^^^^^^^^^^^

There are restrictions on the type of edge selections that can be operated upon.
Invalid selections are:

Loop crosses itself
   This means that the tool could not find any suitable faces that were adjacent to the selected edge(s).
   An example that shows this is selecting two edges that share the same face.
   A face cannot be adjacent to itself.
Multiple edge loops
   The selected edges are not in the same edge loop, which means they do not have a common edge.
   You can minimize this error by always selecting edges end-to-end or in a "chain".
   If you select multiple edges just make sure they are connected.
   This will decrease the possibility of getting looping errors.
Border Edges
   When a single edge was selected in a single sided object.
   An edge loop cannot be found because there is only one face.
   Remember, edge loops are loops that span two or more faces.

A general rule of thumb is that if multiple edges are selected they should be connected end-to-end
such that they form a continuous chain. This is *literally* a general rule because you
can still select edges in a chain that are invalid because some of the edges in the chain are
in different edge loops.


.. _modeling-meshes-editing-edges-rotate:
.. _bpy.ops.mesh.edge_rotate:

Rotate Edge
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Rotate Edge CW / Rotate Edge CCW`

Rotating an edge clockwise (CW) or counter-clockwise (CCW) spins an edge between two faces around their vertices.
This is very useful for restructuring a mesh's topology.

The tool operates on selected edges or the shared edge between selected faces.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_edge-flip-before.png
          :width: 320px

          Selected edge.

     - .. figure:: /images/modeling_meshes_editing_edges_edge-flip-after.png
          :width: 320px

          Edge, rotated CW.

.. warning::

   To rotate an edge based on faces you must select adjacent face pairs,
   otherwise Blender notifies you with an error message,
   *"Could not find any select edges that can be rotated"*. Using either *Rotate Edge CW*
   or *Rotate Edge CCW* will produce exactly the same results as if you had
   selected the common edge.


.. _bpy.ops.mesh.edge_split:

Edge Split
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Edge Split`

*Edge Split* is similar to the *Rip* tool. When two or more touching interior edges,
or a border edge is selected when using *Edge Split*,
a hole will be created, and the selected edges will be duplicated to form the border of the hole.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_edge-split-before.png
          :width: 320px

          Selected edges.

     - .. figure:: /images/modeling_meshes_editing_edges_edge-split-after.png
          :width: 320px

          Adjacent face moved to reveal hole left by split.


.. _bpy.ops.mesh.bridge-edge-loops:
.. _modeling-meshes-editing-bridge-edge-loops:

Bridge Edge Loops
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edge --> Bridge Edge Loops`

*Bridge Edge Loops* connects multiple edge loops with faces.

Connect Loops
   Open Loop
      Loops connected with open ends.
   Closed Loop
      Tries to connect to a circular loop (where start and end are merged).
   Loop pairs
      Connects each even count of loops individually.
Merge
   Merges edge loops rather than creating a new face.
Merge Factor
   Which edge loop the edges are merged to, a value of 0.5 will merge at a half-way point.
Twist
   Determines which vertices in both loops are connected to each other.
Number of Cuts
   The number of intermediate edge loops used to bridge the distance between two loops.
Interpolation
   Linear, Blend Path, Blend Surface
Smoothness
   Smoothness of the *Blend Path* and *Blend Surface*.
Profile Factor
   How much intermediary new edges are shrunk/expanded.
Profile Shape
   The shape of the new edges. See the
   :ref:`Proportional Editing <3dview-transform-control-proportional-edit-falloff>`
   page for a description of each option.


Examples
--------

Simple example showing two closed edge loops.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_bridge-simple-before.png
          :width: 320px

          Input.

     - .. figure:: /images/modeling_meshes_editing_edges_bridge-simple-after.png
          :width: 320px

          Bridge result.

Example of the Bridge tool between edge loops with different numbers of vertices.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_bridge-uneven-before.png
          :width: 320px

          Input.

     - .. figure:: /images/modeling_meshes_editing_edges_bridge-uneven-after.png
          :width: 320px

          Bridge result.

Example using the Bridge tool to cut holes in face selections and connect them.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_bridge-faces-before.png
          :width: 320px

          Input.

     - .. figure:: /images/modeling_meshes_editing_edges_bridge-faces-after.png
          :width: 320px

          Bridge result.

Example showing how Bridge tool can detect multiple loops and connect them in one step.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_bridge-multi-before.png
          :width: 320px

          Input.

     - .. figure:: /images/modeling_meshes_editing_edges_bridge-multi-after.png
          :width: 320px

          Bridge result.

Example of the subdivision option and surface blending with UV's.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_edges_bridge-advanced-before.png
          :width: 320px

          Input.

     - .. figure:: /images/modeling_meshes_editing_edges_bridge-advanced-after.png
          :width: 320px

          Bridge result.
