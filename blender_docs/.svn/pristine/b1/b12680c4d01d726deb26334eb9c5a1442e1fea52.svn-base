
*********
Selecting
*********

There are many ways to select elements, and it depends on what *Mesh Select Mode*
you are in as to what selection tools are available.
First we will go through these modes and after that a look is taken at basic selection tools.


Selection Modes
===============

Select Mode Header Buttons
--------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`3D View Header --> Select Mode`
   :Hotkey:    :kbd:`1`, :kbd:`2`, :kbd:`3`
               (:kbd:`Shift`
               `Multiple Selection Modes`_,
               :kbd:`Ctrl` `Expand/Contract Selection`_).

.. figure:: /images/modeling_meshes_selecting_mode-buttons.png
   :align: right
   :width: 200px

   Edit Mode selection buttons.

In *Edit Mode* there are three different selection modes.
You can enter the different modes by selecting one of the three buttons in the header.

Vertices
   In this mode vertices are shown as points.

   Selected vertices are displayed in orange, unselected vertices in black,
   and the active or last selected vertex in white.
Edges
   In this mode the vertices are not shown.

   Instead the selected edges are displayed in orange,
   unselected edges black, and the active or last selected edge in white.
Faces
   In this mode the faces are displayed with a selection point in the middle which is used for selecting a face.

   Selected faces and their selection point are displayed in orange,
   unselected faces are displayed in black, and the active or last selected face is highlighted in white.

When using these buttons, you can make use of modifier keys, see: `Switching Select Mode`_.

Almost all tools are available in all three mesh selection modes.
So you can *Rotate*, *Scale*, *Extrude*, etc. in all modes.
Of course rotating and scaling a *single* vertex will not do anything useful
(*without* setting the pivot point to another location),
so some tools are more or less applicable in some modes.

See Fig. :ref:`fig-mesh-select-intro-selection-modes` for examples of the different modes.


Multiple Selection Modes
^^^^^^^^^^^^^^^^^^^^^^^^

By holding :kbd:`Shift-LMB` when selecting a selection mode,
you can enable multiple *Selection Modes* at once.
This allows you to quickly select Vertices/Edges/Faces,
without first having to switch modes.

.. _fig-mesh-select-intro-selection-modes:

.. list-table:: Selection modes.

   * - .. figure:: /images/modeling_meshes_selecting_vertex-mode-example.png
          :width: 310px

          Vertex mode example.

     - .. figure:: /images/modeling_meshes_selecting_edge-mode-example.png
          :width: 310px

          Edge mode example.

   * - .. figure:: /images/modeling_meshes_selecting_face-mode-example.png
          :width: 310px

          Face mode example.

     - .. figure:: /images/modeling_meshes_selecting_mixed-mode-example.png
          :width: 310px

          Mixed mode example.


Switching Select Mode
---------------------

When switching modes in an "ascendant" way (i.e. from simpler to more complex), from
*Vertices* to *Edges* and from *Edges* to *Faces*,
the selected parts will still be selected if they form a complete element in the new mode.

For example, if all four edges in a face are selected,
switching from *Edges* mode to *Faces* mode will keep the face selected.
All selected parts that do not form a complete set in the new mode will be unselected.

.. list-table::

   * - .. figure:: /images/modeling_meshes_selecting_edge-mode-example.png
          :width: 310px

          Edge mode, the initial selection.

     - .. figure:: /images/modeling_meshes_selecting_face-mode-switched-from-edge.png
          :width: 310px

          Switching to Face mode.

Hence, switching in a "descendant" way (i.e. from more complex to simpler),
all elements defining the "high-level" element (like a face) will be selected
(the four vertices or edges of a quadrangle, for example).


Expand/Contract Selection
^^^^^^^^^^^^^^^^^^^^^^^^^

By holding :kbd:`Ctrl` when selecting a higher selection mode,
all elements touching the current selection will be added,
even if the selection does not form a complete higher element.

Or contracting the selection when switching to a lower mode.

.. list-table::

   * - .. figure:: /images/modeling_meshes_selecting_vertex-mode-example.png
          :width: 310px

          Vertex mode, the initial selection.

     - .. figure:: /images/modeling_meshes_selecting_edge-mode-expanding-from-vertex.png
          :width: 310px

          Expanding to Edge mode.


X-Ray
=====

The :ref:`x-ray <3dview-shading-xray>` setting is not just for shading, it impacts selection too.

When enabled, selection isn't occluded by the objects geometry
(as if the object was solid).

.. list-table::

   * - .. figure:: /images/modeling_meshes_selecting_limit-selection-to-visible-off.png
          :width: 310px

          X-ray enabled.

     - .. figure:: /images/modeling_meshes_selecting_limit-selection-to-visible-on.png
          :width: 310px

          X-ray disabled.


Select Menu
===========

All :kbd:`A`
   Select all.
None :kbd:`Alt-A`
   Select none.
Inverse :kbd:`Ctrl-I`
   Selects all the geometry that is not selected, and deselect currently selected components.

------------------------

:ref:`Box Select <tool-select-box>` :kbd:`B`
   Interactive box selection.
:ref:`Circle Select <tool-select-circle>` :kbd:`C`
   Interactive circle selection.

------------------------

Select Random
   Selects a random group of vertices, edges, or faces, based on a percentage value.
:ref:`Checker Deselect <modeling-selecting-checker_deselect>`
   De-select alternate elements relative to the active item.

------------------------

Select Sharp Edges
   This tool selects all edges between two faces forming an angle greater than the angle value,
   Where an increasing angle selects sharper edges.

------------------------

`Select Similar`_ :kbd:`Shift-G`
   Select elements similar to the current selection.

------------------------

`Select All by Trait`_
   Select geometry by querying it's characteristics.

------------------------

Select More/Less
   More :kbd:`Ctrl-NumpadPlus`
      Expands the selection to the adjacent elements of the selection type.
   Less :kbd:`Ctrl-NumpadMinus`
      Contracts the selection from the adjacent elements of the selection type.
   Next Active :kbd:`Shift-Ctrl-NumpadPlus`
      This uses selection history to select the next vertex/edge/face based on surrounding topology.
   Previous Active :kbd:`Shift-Ctrl-NumpadMinus`
      Select previous just removes the last selected element.

------------------------

Select Loops
   `Edge Loops`_
      Select connected edges.
   `Face Loops`_
      Select connected faces.
   `Edge Boundary`_
      Select boundary edges.
   `Edge Ring`_
      Select connected edge ring.

------------------------

Select Linked
   `Select Linked`_
      Selects all components that are connected to the current selection (see `Select Linked`_).
   `Shortest Path`_
      Path between two selected elements.
   Linked Flat Faces
      Select connected faces based on a threshold of the angle between them.
      This is useful for selecting faces that are planar.

------------------------

Select Side of Active
   Selects all vertices on the mesh in a single axis relative to the active vertex.
   In Vertex selection mode only.
Mirror Selection :kbd:`Shift-Ctrl-M`
   Select mesh items at the mirrored location across the chosen axis.


Selection Tools
===============

.. _modeling-selecting-checker_deselect:

Checker Deselect
----------------

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


Select All by Trait
-------------------

.. _mesh-select-non-manifold:

Non Manifold
   Selects the :term:`non-manifold` geometry of a mesh.
   This entry is available when editing a mesh, in Vertex and Edge selection modes only.

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

Loose Geometry
   Selects all vertices or edges that do not form part of a face.
Interior Faces
   Selects faces where all edges have more than two faces.
Faces by Sides
   Selects all faces that have a specified number of edges.

------------------------

Ungrouped Vertices
   Selects all vertices which are not part of
   a :doc:`vertex group </modeling/meshes/properties/vertex_groups/index>`.


Select Linked
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Linked`
   :Hotkey:    :kbd:`Ctrl-L`

Select geometry connected to already selected elements.
This is often useful when a mesh has disconnected, overlapping parts,
where isolating it any other way would be tedious.

To give more control, you can also enable delimiters in the :ref:`ui-undo-redo-adjust-last-operation` panel,
so the selection is constrained by seams, sharp edges, materials or UV islands.

With *Pick Linked* you can also select connected geometry directly under the cursor,
using the :kbd:`L` shortcut to select or :kbd:`Shift-L` to deselect linked.

This works differently in that it uses the geometry under the cursor instead of the existing selection.


Select Similar
--------------

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


.. _modeling-meshes-selecting-edge-loops:

Edge Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Vertex or Edge select mode
   :Menu:      :menuselection:`Select --> Select Loops --> Edge Loops`
   :Hotkey:    :kbd:`Alt-LMB`, or :kbd:`Shift-Alt-LMB` for modifying existing selection.

Holding :kbd:`Alt` while selecting an edge selects a loop of edges that are connected in
a line end-to-end, passing through the edge under the mouse pointer.
Holding :kbd:`Shift-Alt` while clicking adds to the current selection.

Edge loops can also be selected based on an existing edge selection,
using either :menuselection:`Select --> Edge Loop`.

.. note:: *Vertex* mode

   In *Vertex* select mode, you can also select edge loops, by using the same hotkeys,
   and clicking on the *edges* (not on the vertices).

.. figure:: /images/modeling_meshes_selecting_edge-loops.png

   Longitudinal and latitudinal edge loops.

The left sphere shows an edge that was selected longitudinally. Notice how the loop is open.
This is because the algorithm hit the vertices at the poles and is terminated
because the vertices at the pole connect to more than four edges. However,
the right sphere shows an edge that was selected latitudinally and has formed a closed loop.
This is because the algorithm hit the first edge that it started with.


.. _modeling-meshes-selecting-face-loops:

Face Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Face or Vertex select modes
   :Hotkey:    :kbd:`Alt-LMB` or :kbd:`Shift-Alt-LMB` for modifying existing selection.

In face select mode, holding :kbd:`Alt` while selecting an *edge* selects a loop of
faces that are connected in a line end-to-end, along their opposite edges.

In vertex select mode,
the same can be accomplished by using :kbd:`Ctrl-Alt` to select an edge,
which selects the face loop implicitly.

.. figure:: /images/modeling_meshes_selecting_face-loops.png

   Face loop selection.

This face loop was selected by clicking with :kbd:`Alt-LMB` on an edge,
in *face* select mode.
The loop extends perpendicular from the edge that was selected.

.. figure:: /images/modeling_meshes_selecting_face-loops-vertex.png

   :kbd:`Alt` versus :kbd:`Ctrl-Alt` in vertex select mode.

A face loop can also be selected in *Vertex* select mode.
Technically :kbd:`Ctrl-Alt-LMB` will select an *Edge Ring*,
however, in *Vertex* select mode, selecting an *Edge Ring* implicitly
selects a *Face Loop* since selecting opposite edges of a face implicitly selects
the entire face.


Edge Boundary
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Vertex or Edge select modes
   :Hotkey:    :kbd:`Alt-LMB`

Loop selection on edge boundaries.
To extend the selection to all boundaries if the current boundary is already selected
use :kbd:`Alt-LMB` again.


Edge Ring
---------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select Loops --> Edge Rings`
   :Hotkey:    :kbd:`Ctrl-Alt-LMB`

In *Edge* select mode, holding :kbd:`Ctrl-Alt`
while selecting an edge (or two vertices) selects a sequence of edges that are not connected,
but on opposite sides to each other continuing along a :doc:`face loop </modeling/meshes/structure>`.

As with edge loops, you can also select edge rings based on current selection,
using either :menuselection:`Select --> Select Loops --> Edge Rings`.

.. note:: *Vertex* mode

   In *Vertex* select mode, you can use the same hotkeys when *clicking on the edges* (not on the vertices),
   but this will directly select the corresponding face loop...

.. _fig-mesh-select-advanced-loop-ring:

.. figure:: /images/modeling_meshes_selecting_edge-ring.png

   A selected edge loop, and a selected edge ring.

In Fig. :ref:`fig-mesh-select-advanced-loop-ring` the same edge was clicked on,
but two different "groups of edges" were selected, based on the different tools.
One is based on edges during computation and the other is based on faces.

.. note:: Convert Selection to Whole Faces

   If the edge ring selection happened in Edge Select Mode, switching to Face Select Mode will erase the selection.

   This is because none of those faces had all its (four) edges selected,
   just two of them.

   Instead of selecting the missing edges manually or by using :kbd:`Shift-Alt-` twice,
   it is easier to first switch to Vertex Select Mode, which will kind of "flood" the selection.
   A subsequent switch to Face Select Mode will then properly select the faces.


Shortest Path
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select Linked --> Shortest Path`
   :Hotkey:    :kbd:`Ctrl-LMB`

.. figure:: /images/modeling_meshes_selecting_shortest-path.png

   Select a face or vertex path with :kbd:`Ctrl-LMB`.

Selects all geometry along the shortest path from
the active vertex/edge/face to the one which was selected.

Face Stepping
   Supports diagonal paths for vertices and faces, and
   selects edge rings with edges.
Topological Distance
   Which only takes into account the number of edges of the path and
   not the length of the edges to calculate the distances.
Fill Region :kbd:`Shift-Ctrl-LMB`
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
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Edge select mode
   :Menu:      :menuselection:`Select --> Select Loops --> Select Loop Inner-Region`

*Select Loop Inner-Region* selects all faces that are inside a closed loop of edges.
While it is possible to use this operator in *Vertex* and *Face* selection modes, results may be unexpected.
Note that if the selected loop of edges is not closed,
then all connected edges on the mesh will be considered inside the loop.

.. figure:: /images/modeling_meshes_selecting_inner-region1.png

   Loop to Region.

.. figure:: /images/modeling_meshes_selecting_inner-region2.png

   This tool handles multiple loops fine, as you can see.

.. figure:: /images/modeling_meshes_selecting_inner-region3.png

   This tool handles "holes" just fine as well.


Boundary Loop
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode --> Edge select mode
   :Menu:      :menuselection:`Select --> Select Loops --> Select Boundary Loop`

*Select Boundary Loop* does the opposite of *Select Loop Inner-Region*,
based on all regions currently selected, it selects only the edges at the border(contour) of these islands.
It can operate in any select mode, but when in *Face* mode it will switch to *Edge* select mode after running.

All this is much more simple to illustrate with examples:

.. figure:: /images/modeling_meshes_selecting_boundary-loop.png

   Select Boundary Loop does the opposite and forces into Edge Select Mode.


Known Issues
============

N-Gons in Face Select Mode
--------------------------

.. figure:: /images/modeling_meshes_selecting_face-mode-ngon-visual-problem.png

   N-gon face having its center dot inside another face.

As already known, faces are marked with a little square dot in the middle of the face.
With n-gons that can lead in certain cases to a confusing display.
The example shows the center dot of the U-shaped n-gon being inside of the oblong face inside the "U".
It is not easy to say which dot belongs to which face (the orange dot in the image is the object origin).
Luckily, you do not need to care much, because to select a face, you do not have to click the center dot,
but the face itself.
