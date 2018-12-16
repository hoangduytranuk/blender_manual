
*****
Bevel
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Edges --> Bevel` or :menuselection:`Specials --> Bevel`
   :Hotkey:    :kbd:`Ctrl-B`
   :Menu:      :menuselection:`Mesh --> Vertices --> Bevel` (vertex-only)
   :Hotkey:    :kbd:`Shift-Ctrl-B` (vertex-only)

The *Bevel* tool allows you to create chamfered or rounded corners to geometry.
A bevel is an effect that smooths out edges and corners.

True world edges are very seldom exactly sharp.
Not even a knife blade edge can be considered perfectly sharp.
Most edges are intentionally beveled for mechanical and practical reasons.

Bevels are also useful for giving realism to non-organic models. In the real world,
the blunt edges on objects catch the light and change the shading around the edges.
This gives a solid, realistic look,
as opposed to un-beveled objects which can look too perfect.

.. figure:: /images/modeling_meshes_editing_subdividing_bevel_cubes.jpg

   Cubes with and without bevel.


Usage
=====

The *Bevel* tool works only on selected edges with exactly two adjacent faces.
It will recognize any edges included in a vertex or face selection as well,
and perform the bevel the same as if those edges were explicitly selected.
In "vertex only" mode, the *Bevel* tool works on selected vertices instead of edges.
The *Bevel* tool smooths the edges and/or "corners" (vertices)
by replacing them with faces making smooth profiles with a specified number of *segments*
(see the options below for details about the bevel algorithm).

Use :kbd:`Ctrl-B` or a method listed above to run the tool.
Move the mouse to interactively specify the bevel offset,
and scroll the :kbd:`Wheel` to increase or decrease the number of segments (see below).

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-1.png
          :width: 320px

          Selected edge before beveling.

     - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-2.png
          :width: 320px

          Result of bevel (one segment).

     - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-3.png
          :width: 320px

          Result of bevel (vertex only).

.. note::

   Normal (edge) beveling only works on edges that have exactly two faces
   attached to them. Vertex beveling has no such restriction.


Options
=======

.. figure:: /images/modeling_meshes_editing_subdividing_bevel_panel.png
   :align: right

Amount
   You can change the bevel amount by moving the mouse towards and away from the object,
   a bit like with transform tools.
   The exact meaning of the value depends on the *Amount Type* option (see below).
   As usual, the scaling can be controlled to a finer degree by holding :kbd:`Shift` to scale in 0.001 steps.
   :kbd:`LMB` finalizes the operation, :kbd:`RMB` or :kbd:`Esc` aborts the action.

Amount Type :kbd:`M`
   Selects how the *Amount* value controls the size of the bevel. According to the selection, the amount is:

   Offset
      The distance of a new edge from the original.
   Width
      The width of the bevel face.
   Depth
      The perpendicular distance from the original edge to the bevel face.
   Percent
      The percentage of the length of adjacent edges that the new edges slide.

Segments :kbd:`S`
   The number of segments in the bevel can be defined by
   scrolling the mouse :kbd:`Wheel` to increase or decrease this value.
   The greater the number of segments, the smoother the bevel.
   Or press :kbd:`S` to change the number with mouse movements, as well as numeric input.

   Alternatively, you can manually enter a segment number value while using the tool,
   or in the Mesh Tool options panel after using the tool.

   .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-4.png
      :width: 320px

      Bevel with four segments.

Profile :kbd:`P`
   This is a number between 0 and 1 that controls the shape of the profile (side view of a beveled edge).
   The default value, 0.5, gives a circular arc (if the faces meet at right angles).
   Values less than that give a flatter profile, with 0.25 being exactly flat,
   and values less than that giving a concave bevel.
   Values more than 0.5 give a more convex profile.
   Similarly as *Segments* it can be set with mouse movements and numeric input after toggling :kbd:`P`.
Vertex Only :kbd:`V`
   When selected, the tool is in "vertex only" mode, and only vertices will be beveled.
Clamp Overlap :kbd:`C`
   When selected, the bevel amount is not allowed to go larger than an amount that causes
   overlapping collisions with other geometry.
Loop Slide
   If there are unbeveled edges along with beveled edges into a vertex,
   the bevel tries to slide along those edges when possible.
   Turning the option off can lead to more even bevel widths.
Material
   The *Material* number specifies which material should be assigned to the new faces created by the *Bevel* tool.
   With the default, -1, the material is inherited from the closest existing face ("closest" can be a bit ambiguous).
   Otherwise, the number is the slot index of the material to use for all newly created faces.


Examples
========

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-5.png
          :width: 320px

          Result of beveling multiple edges.

     - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-6.png
          :width: 320px

          Another example of beveling multiple edges.

     - .. figure:: /images/modeling_meshes_editing_subdividing_bevel_example-7.png
          :width: 320px

          An example using Profile=0.150.

.. seealso:: Bevel Modifier

   The :doc:`Bevel Modifier </modeling/modifiers/generate/bevel>`
   is a non-destructive alternative to the Bevel tool.
