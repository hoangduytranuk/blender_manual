..    TODO/Review: {{review|partial=X|text= expand advanced selection tools|im=examples}}.

********
Advanced
********

The select menu in edit mode contains additional tool for selecting components:

Sharp Edges
   This tool selects all edges between two faces forming an angle greater than the angle value,
   Where an increasing angle selects sharper edges.
Linked Flat Faces :kbd:`Shift-Ctrl-Alt-F`
   Select connected faces based on a threshold of the angle between them.
   This is useful for selecting faces that are planar.
Mirror
   Select mesh items at the mirrored location across the chosen axis.
Side of Active
   Selects all vertices on the mesh in a single axis relative to the active vertex.
   In Vertex selection mode only.
Linked
   Selects all components that are connected to the current selection (see `Select Linked`_).


Checker Deselect
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Checker Deselect`

This tool applies an alternating selected/deselected checker pattern.
This only works if you already have more than one mesh element selected.

Changes the current selection so that only every Nth elements (vertices, edges or faces,
depending on the active selection mode) will remain selected, starting from the active one.

In case of islands of selected elements, this tool will affect
only the island of the active element (if there is one), or the island of the first element
in the order of internal storage (if there is no active element).

Nth Selection
   Skip every Nth element leaving it selected.
Skip
   Number of consecutive elements to skip (keep selected) at once.
Offset
   Offset from the starting point.


Select All by Traits
====================

.. _mesh-select-non-manifold:

Non Manifold :kbd:`Shift-Ctrl-Alt-M`
   Selects the :term:`non-manifold` geometry of a mesh.
   This entry is available when editing a mesh, in Vertex and Edge selection modes only.
   The Operator panel provides several selection options:

   Extend
      Lets you extend the current selection.
   Wire
      Selects all the edges that do not belong to any face.
   Boundaries
      Selects edges in boundaries and holes.
   Multiple Faces
      Selects edges that belong to three or more faces.
   Non Contiguous
      Selects edges that belong to exactly two faces with opposite normals.
   Vertices
      Selects vertices that belong to *wire* and *multiple face* edges, isolated vertices,
      and vertices that belong to non-adjoining faces.
Interior Faces
   Selects faces where all edges have more than two faces.
Select Faces by Sides
   Selects all faces that have a specified number of edges.
Loose Geometry
   Selects all vertices or edges that do not form part of a face.
Ungrouped Vertices
   Selects all vertices which are not part of
   a :doc:`vertex group </modeling/meshes/properties/vertex_groups/index>`.


Select Linked
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Linked`
   :Hotkey:    :kbd:`Ctrl-L`

Select geometry connected to already selected elements.
This is often useful when a mesh has disconnected, overlapping parts,
where isolating it any other way would be tedious.

To give more control, you can also enable delimiters in the Operator panel,
so the selection is constrained by seams, sharp edges, materials or UV islands.

With *Pick Linked* you can also select connected geometry directly under the cursor,
using the :kbd:`L` shortcut to select or :kbd:`Shift-L` to deselect linked.

This works differently in that it uses the geometry under the cursor instead of the existing selection.


Select Similar
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Similar...`
   :Hotkey:    :kbd:`Shift-G`

Select geometry that has similar certain properties to the ones selected,
based on a threshold that can be set in tool properties after activating the tool.
Tool options change depending on the selection mode:

Vertex Selection Mode:
   Normal
      Selects all vertices that have normals pointing in similar directions to those currently selected.
   Amount of Adjacent Faces
      Selects all vertices that have the same number of faces connected to them.
   Vertex Groups
      Selects all vertices in the same :doc:`vertex group </modeling/meshes/properties/vertex_groups/index>`.
   Amount of Connecting Edges
      Selects all vertices that have the same number of edges connected to them.
   Face Regions
      Select matching features on a mesh that has multiple similar areas based on the topology.

Edge Selection Mode:
   Length
      Selects all edges that have a similar length as those already selected.
   Direction
      Selects all edges that have a similar direction (angle) as those already selected.
   Amount of Faces Around an Edge
      Selects all edges that belong to the same number of faces.
   Face Angles
      Selects all edges that are between two faces forming a similar angle, as with those already selected.
   Crease
      Selects all edges that have a similar :ref:`Crease <modeling-edges-crease-subdivision>`
      value as those already selected.
   Bevel
      Selects all edges that have the same *Bevel Weight* as those already selected.
   Seam
      Selects all edges that have the same *Seam* state as those already selected.
      *Seam* is a true/false setting used in :ref:`UV texturing <editors-uv-index>`.
   Sharpness
      Selects all edges that have the same *Sharp* state as those already selected.
      *Sharp* is a true/false setting (a flag) used by
      the :doc:`Edge Split Modifier </modeling/modifiers/generate/edge_split>`.

Face Selection Mode:
   Material
      Selects all faces that use the same material as those already selected.
   Image
      Selects all faces that use the same UV texture as those already selected
      (see :ref:`UV texturing <editors-uv-index>` pages).
   Area
      Selects all faces that have a similar area as those already selected.
   Polygon Sides
      Selects all faces that have the same number of edges.
   Perimeter
      Selects all faces that have a similar perimeter (added values of its edge lengths).
   Normal
      Selects all faces that have a similar normal as those selected.
      This is a way to select faces that have the same orientation (angle).
   Co-planar
      Selects all faces that are (nearly) in the same plane as those selected.

.. (todo) check type: Image in Cycles


More/Less
=========

More :kbd:`Ctrl-NumpadPlus`
   Expands the selection to the adjacent elements of the selection type.
Less :kbd:`Ctrl-NumpadMinus`
   Contracts the selection from the adjacent elements of the selection type.

.. TODO2.8 how to handle face step.

Next Active :kbd:`Shift-Ctrl-NumpadPlus`
   This uses selection history to select the next vertex/edge/face based on surrounding topology.
Previous Active :kbd:`Shift-Ctrl-NumpadMinus`
   Select previous just removes the last selected element.


Select Loops
============

You can easily select loops of components:


Edge Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Vertex or Edge select mode
   :Menu:      :menuselection:`Select --> Edge Loop`
   :Hotkey:    :kbd:`Alt-RMB`

Holding :kbd:`Alt` while selecting an edge selects a loop of edges that are connected in
a line end-to-end, passing through the edge under the mouse pointer.
Holding :kbd:`Shift-Alt` while clicking adds to the current selection.

Edge loops can also be selected based on an existing edge selection,
using either :menuselection:`Select --> Edge Loop`,
or the *Edge Loop Select* option of the *Edge Specials* menu :kbd:`Ctrl-E`.

.. note:: *Vertex* mode

   In *Vertex* select mode, you can also select edge loops, by using the same hotkeys,
   and clicking on the *edges* (not on the vertices).

.. figure:: /images/modeling_meshes_selecting_advanced_edge-loops.png

   Longitudinal and latitudinal edge loops.

The left sphere shows an edge that was selected longitudinally. Notice how the loop is open.
This is because the algorithm hit the vertices at the poles and terminated
because the vertices at the pole connect to more than four edges. However,
the right sphere shows an edge that was selected latitudinally and has formed a closed loop.
This is because the algorithm hit the first edge that it started with.


Face Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Face or Vertex select modes
   :Hotkey:    :kbd:`Alt-RMB`

In face select mode, holding :kbd:`Alt` while selecting an *edge* selects a loop of
faces that are connected in a line end-to-end, along their opposite edges.

In vertex select mode,
the same can be accomplished by using :kbd:`Ctrl-Alt` to select an edge,
which selects the face loop implicitly.

.. figure:: /images/modeling_meshes_selecting_advanced_face-loops.png

   Face loop selection.

This face loop was selected by clicking with :kbd:`Alt-RMB` on an edge,
in *face* select mode.
The loop extends perpendicular from the edge that was selected.

.. figure:: /images/modeling_meshes_selecting_advanced_face-loops-vertex.png

   :kbd:`Alt` versus :kbd:`Ctrl-Alt` in vertex select mode.

A face loop can also be selected in *Vertex* select mode.
Technically :kbd:`Ctrl-Alt-RMB` will select an *Edge Ring*,
however, in *Vertex* select mode, selecting an *Edge Ring* implicitly
selects a *Face Loop* since selecting opposite edges of a face implicitly selects
the entire face.


Edge Boundary
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Vertex or Edge select modes
   :Hotkey:    :kbd:`Alt-RMB`

Loop selection on edge boundaries.
To extend the selection to all boundaries if the current boundary is already selected
use :kbd:`Alt-RMB` again.


Edge Ring
---------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Edge Ring`
   :Hotkey:    :kbd:`Ctrl-Alt-RMB`

In *Edge* select mode, holding :kbd:`Ctrl-Alt`
while selecting an edge (or two vertices) selects a sequence of edges that are not connected,
but on opposite sides to each other continuing along a :doc:`face loop </modeling/meshes/structure>`.

As with edge loops, you can also select edge rings based on current selection,
using either :menuselection:`Select --> Edge Ring`,
or the *Edge Ring Select* option of the *Edge Specials* menu :kbd:`Ctrl-E`.

.. note:: *Vertex* mode

   In *Vertex* select mode, you can use the same hotkeys when *clicking on the edges* (not on the vertices),
   but this will directly select the corresponding face loop...

.. _fig-mesh-select-advanced-loop-ring:

.. figure:: /images/modeling_meshes_selecting_advanced_edge-ring.png

   A selected edge loop, and a selected edge ring.

In Fig. :ref:`fig-mesh-select-advanced-loop-ring` the same edge was clicked on,
but two different "groups of edges" were selected, based on the different tools.
One is based on edges during computation and the other is based on faces.


Shortest Path
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Shortest Path`
   :Hotkey:    :kbd:`Ctrl-RMB`

.. figure:: /images/modeling_meshes_selecting_advanced_shortest-path.png

   Select a face or vertex path with :kbd:`Ctrl-RMB`.

Selects all geometry along the shortest path from the active
vertex/edge/face to the one which was selected.

Face Stepping
   Supports diagonal paths for vertices and faces, and
   selects edge rings with edges.
Topological Distance
   Which only takes into account the number of edges of the path and
   not the length of the edges to calculate the distances.
Fill Region :kbd:`Shift-Ctrl-RMB`
   Selects all elements in the shortest paths from the active selection to the clicked area.
Checker Select Options
   Allows to quickly select alternate elements in a path.

   Nth Selection
      Skip every Nth element, leave unselected.
   Skip
      Number of consecutive elements to skip at once.
   Offset
      Offset from the starting point.


Loop Inner-Region
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Edge select mode
   :Menu:      :menuselection:`Select --> Select Loop Inner-Region`

*Select Loop Inner-Region* selects all faces that are inside a closed loop of edges.
While it is possible to use this operator in *Vertex* and *Face* selection modes, results may be unexpected.
Note that if the selected loop of edges is not closed,
then all connected edges on the mesh will be considered inside the loop.

.. figure:: /images/modeling_meshes_selecting_advanced_inner-region1.png

   Loop to Region.

.. figure:: /images/modeling_meshes_selecting_advanced_inner-region2.png

   This tool handles multiple loops fine, as you can see.

.. figure:: /images/modeling_meshes_selecting_advanced_inner-region3.png

   This tool handles "holes" just fine as well.


Boundary Loop
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Edge select mode
   :Menu:      :menuselection:`Select --> Select Boundary Loop`

*Select Boundary Loop* does the opposite of *Select Loop Inner-Region*,
based on all regions currently selected, it selects only the edges at the border(contour) of these islands.
It can operate in any select mode, but when in *Face* mode it will switch to *Edge* select mode after running.

All this is much more simple to illustrate with examples:

.. figure:: /images/modeling_meshes_selecting_advanced_boundary-loop.png

   Select Boundary Loop does the opposite and forces into Edge Select Mode.
