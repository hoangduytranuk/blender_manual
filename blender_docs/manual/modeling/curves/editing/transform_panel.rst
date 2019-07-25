.. _modeling-curves-transform-panel:

***************
Transform Panel
***************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Sidebar --> Transform`

When nothing is selected, the panel is empty.
When more than one vertex is selected, the median values are edited
and "Median" is added in front of the labels.

Control Point, Vertex
   The first controls (X, Y, Z) show the coordinates of the selected point or handle (vertex).
   In case of a NURBS curve, there is a fourth component available (W),
   which defines the weight of the selected control point or the median weight.
Space
   The Space radio buttons let you choose if those coordinates are relative to the object origin (local) or
   the global origin (global).

   Global, Local

.. _curves-weight:

Weight
   This sets the "goal weight" of selected control points,
   which is used when a curve has :doc:`Soft Body </physics/soft_body/index>` physics,
   forcing the curve to "stick" to their original positions, based on the weight.
   The precise value can be adjusted in the :ref:`ui-undo-redo-adjust-last-operation` Panel.
   To adjust the *Mean Weight* (average) of selected control points use
   :menuselection:`Sidebar region --> Transform --> Mean Weight`.
Radius
   TODO.
Tilt
   TODO.
