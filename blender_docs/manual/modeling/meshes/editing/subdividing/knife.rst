.. _bpy.ops.mesh.knife:
.. _tool-mesh-knife:

**********
Knife Tool
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Add: Knife/Select`
   :Hotkey:    :kbd:`K` or :kbd:`Shift-K`

The Knife tool can be used to interactively subdivide (cut up)
geometry by drawing lines or closed loops to create holes.


Usage
=====

When you press :kbd:`K` (or :kbd:`Shift-K`), the Knife tool becomes active.


Drawing the Cut Line
--------------------

When using *Knife*, the cursor changes to an icon of a scalpel
and the header changes to display options for the tool.
You can draw connected straight lines by clicking :kbd:`LMB`,
marked with small green squares. Red squares are already defined cuts.
Surrounding red squares mean that there is a cut already in that very position,
so no additional vertex will be created (besides the first one).

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_line-before.png
          :width: 200px

          Mesh before knife cut.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_line-active.png
          :width: 200px

          Knife cut active.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_line-after.png
          :width: 200px

          After confirming knife cut.


Options
=======

Knife selection :kbd:`Shift-K`
   Activates the knife with another set of options so only selected faces are cut and
   *Cut through* is on by default.

New cut :kbd:`E`
   Begins a new cut. This allows you to define multiple distinct cut lines.
   If multiple cuts have been defined, they are recognized as new snapping points.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_multiple-before.png
          :width: 320px

          Creating multiple cuts.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_multiple-after.png
          :width: 320px

          Result of starting new cuts while in the tool.

Midpoint snap :kbd:`Ctrl`
   Hold to snap the cursor to the midpoint of edges,
   meaning that all cuts will be performed at the exact center of each cut edge.
Ignore snap :kbd:`Shift`
   Hold to make the tool ignore snapping,
   unlike the default where mouse cursor snaps to near edges.
Cut through: :kbd:`Z`
   Allow the Cut tool to cut through to obscured faces, instead of only the visible ones.
Angle constrain :kbd:`C`
   Constrains the cut to 45 degree increments.
Close loop: double-click :kbd:`LMB`
   This is a quick way to close the loop you are currently cutting.
Draw a continuous line: :kbd:`LMB` drag.
   So you can draw a free-hand line over a surface,
   points will be created at edge intersections.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_angle-before.png
          :width: 320px

          Constraining cut angle.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_angle-after.png
          :width: 320px

          Result of constraining cut angle.


Confirming and Selection
========================

Pressing :kbd:`Esc` or :kbd:`RMB` at any time cancels the tool,
and pressing :kbd:`LMB` or :kbd:`Return` confirms the cut, with the following options:

:kbd:`Return` will leave selected every edge except the new edges created from the cut.


Knife Project
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Add: Knife Project`

Knife projection is a non-interactive tool where you can use objects to cookie-cut into
the mesh rather than hand drawing the line.

This works by using the outlines of other selected objects in Edit Mode to cut into the mesh
along the view axis, resulting geometry inside the cutters outline will be selected.

Outlines can be wire or boundary edges.

To use Knife Project, first while in *Object Mode*, select the "cutting object"
then add to that selection with :kbd:`Shift-RMB` the "object to be cut".
Now, enter *Edit Mode* and press *Knife Project* (found in the Toolbar).

.. seealso::

   :doc:`3D View Alignment </editors/3dview/navigate/align>` to adjust the projection axis.


Examples
--------

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-text-before.jpg
          :width: 320px

          Before projecting from a text object.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-text-after.jpg
          :width: 320px

          Resulting knife projection.

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-mesh-before.jpg
          :width: 320px

          Before projecting from a mesh object.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-mesh-after.jpg
          :width: 320px

          Resulting knife projection (extruded after).

   * - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-curve-before.png
          :width: 320px

          Before projecting from a 3D curve object.

     - .. figure:: /images/modeling_meshes_editing_subdividing_knife_project-curve-after.jpg
          :width: 320px

          Resulting knife projection (extruded after).


Known Limitations
=================

Duplicate Vertices
------------------

If you experience problems where duplicate vertices are being created by cuts,
this is often caused by too large a near/far clipping range.

Try increasing the *Clip Start* to avoid this problem,
see :ref:`Depth Troubleshooting <troubleshooting-depth>` for details.


Unconnected Cuts
----------------

Cuts that begin or end in the middle of a face, will be ignored.

*This is constrained by the kinds of geometry Blender can represent.*
