.. _bpy.ops.mesh.loopcut_slide:

**************
Loop Subdivide
**************

.. _tool-mesh-loop_cut:

Loop Cut and Slide
==================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Add: Loop Cut and Slide`
   :Hotkey:    :kbd:`Ctrl-R`

*Loop Cut and Slide* splits a loop of faces by inserting a new edge loop intersecting the chosen edge.


Usage
-----

The tool is interactive and has two steps:


Pre-visualizing the Cut
^^^^^^^^^^^^^^^^^^^^^^^

After the tool is activated, move the cursor over a desired edge.
The cut to be made is marked with a magenta colored line as you move the mouse over the various edges.
The to be created edge loop stops at the poles (tris and n-gons) where the existing face loop terminates.


Sliding the new Edge Loop
^^^^^^^^^^^^^^^^^^^^^^^^^

Once an edge is chosen via :kbd:`LMB`,
you can move the mouse along the edge to determine where the new edge loop will be placed.
This is identical to the :ref:`Edge Slide tool <modeling-meshes-editing-edge-slide>`.
Clicking :kbd:`LMB` again confirms and makes the cut at the pre-visualized location,
or clicking :kbd:`RMB` forces the cut to exactly 50%.
This step is skipped when using multiple edge loops (see below).

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_loop_before.png
          :width: 200px

          Mesh before inserting edge loop.

     - .. figure:: /images/modeling_meshes_editing_subdividing_loop_preview.png
          :width: 200px

          Preview of edge loop location.

     - .. figure:: /images/modeling_meshes_editing_subdividing_loop_placement.png
          :width: 200px

          Interactive placement of edge loop between adjacent loops.


Options
-------

The options are available while the tool is in use, and later in the :ref:`ui-undo-redo-adjust-last-operation` panel.


Loop Cut
^^^^^^^^

Number of Cuts :kbd:`Wheel` or :kbd:`PageUp` / :kbd:`PageDown`
   After activating the tool, but before confirming initial loop location,
   you can increase and decrease the number of cuts to create,
   by entering a number with the keyboard, scrolling :kbd:`Wheel` or using :kbd:`PageUp` and :kbd:`PageDown`.

   .. note::

      When creating multiple loops, these cuts are uniformly distributed in the original face loop,
      and you will *not* be able to control their positions.

   .. list-table::

      * - .. figure:: /images/modeling_meshes_editing_subdividing_loop_multicut.png
             :width: 250px

             Preview of multiple edge loops.

        - .. figure:: /images/modeling_meshes_editing_subdividing_loop_multicut-after.png
             :width: 250px

             Result of using multiple cuts.

Smoothness :kbd:`Alt-Wheel`
   Smoothing causes edge loops to be placed in an interpolated position, relative to the face it is added to,
   causing them to be shifted outwards or inwards by a given percentage,
   similar to the *Subdivide Smooth* tool. When not using smoothing,
   new vertices for the new edge loop are placed exactly on the pre-existing edges.
   This keeps subdivided faces flat, but can distort geometry,
   particularly when using :doc:`Subdivision Surfaces </modeling/modifiers/generate/subdivision_surface>`.
   Smoothing can help maintain the curvature of a surface once it is subdivided.

   .. list-table::

      * - .. figure:: /images/modeling_meshes_editing_subdividing_loop_unsmooth.png
             :width: 250px

             Added edge loops without smoothing.

        - .. figure:: /images/modeling_meshes_editing_subdividing_loop_smooth.png
             :width: 250px

             Same edge loops, but with smoothing value.

Falloff
   Falloff type for *Smoothness*, changes the shape of the profile.


Edge Slide
^^^^^^^^^^

Even :kbd:`E`
   Only available for single edge loops.
   This matches the shape of the edge loop to one of the adjacent edge loops.
   (See :ref:`Edge Slide tool <modeling-meshes-editing-edge-slide>` for details.)
Flip :kbd:`F`
   When Even is enabled, this flips the target edge loop to match.
   (See :ref:`Edge Slide tool <modeling-meshes-editing-edge-slide>` for details.)


Offset Edge Slide
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Add: Offset Edge Slide`
   :Hotkey:    :kbd:`Shift-Ctrl-R`

Add two edge loops on either side of selected loops.

Cap Endpoint
   Extends the loop by creating triangles at endpoints.
Edge Slide
   See :ref:`Edge Slide tool <modeling-meshes-editing-edge-slide>`.


Subdivide Edge-Ring
===================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Mesh --> Edges --> Subdivide Edge-Ring`

Take an edge ring, and subdivide with interpolation options.

Options
   See :ref:`Bridge Edge Loops <modeling-meshes-editing-bridge-edge-loops>`.
