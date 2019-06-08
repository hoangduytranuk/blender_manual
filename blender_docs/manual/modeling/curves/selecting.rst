
*********
Selecting
*********

Curve selection in *Edit Mode* has fewer options than with meshes.
Mainly this is, because there is only one selectable element type, the control points
(no select mode needed here...). These points are a bit more complex than simple vertices,
however, especially for Béziers, as there is the central vertex, and its two handles...

The basic tools are the same as with :doc:`meshes </modeling/meshes/selecting/introduction>`,
so you can select a simple control point with the :kbd:`RMB`,
add to current selection with :kbd:`Shift-RMB`, Border Select :kbd:`B`, and so on.

One word about the Bézier control points: when you select the main central vertex,
the two handles are automatically selected too, so you can grab it as a whole,
without creating an angle in the curve. However, when you select a handle,
only this vertex is selected, allowing you to modify this control vector...

Note that, unlike mesh edges, you cannot directly select a segment. Instead,
select all of the control points that make up the segment you want to edit.


Select Menu
===========

With curves, all "advanced" selection options are regrouped in the *Select* menu of
the 3D Views header. Let us detail them:

- Random...
- Inverse
- Select/Deselect All

Border/Circle Select
   All these options have the same meaning and behavior as in
   :doc:`Object Mode </scene_layout/object/selecting/tools>`
   (and the specifics of *Border Select* in *Edit Mode* have already been discussed
   :doc:`here </modeling/meshes/selecting/introduction>`).


Select Linked
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select Linked`
   :Hotkey:    :kbd:`L`, :kbd:`Ctrl-L`, :kbd:`Shift-L`

:kbd:`L` (or :kbd:`Ctrl-L` for all) will add to the selection the cursor's nearest control point,
and all the linked ones, i.e. all points belonging to the same curve. Note that for Bézier,
using :kbd:`L` with a handle selected will select the whole control point and all the linked ones.


Select Similar
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select Similar`
   :Hotkey:    :kbd:`Shift-G`

Selects control points that have certain similar properties to the active one.
The Operator panel provides several selection options:

Type
   Type
      Selects splines that have the same spline Type i.e. Bézier, NURBS or Poly.
   Radius
      Selects control points that have a similar Radius value.
   Weight
      Selects all points that have a similar Weight value.
   Direction
      Selects control points that have a similar handles direction.

Compare
   Equal, Greater, Less. (only for Radius, Weight) (ToDo 2.76)
Threshold
   Precision (ToDo 2.76)


Shortest Path
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Operator Search --> Pick Shortest Path`
   :Hotkey:    :kbd:`Ctrl-RMB`

Selects the curve segments between two control points: the active and the one under the cursor.
In the case of a closed curve, the shortest path will be selected.


Select/Deselect First/Last
==========================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select/Deselect First`,
               :menuselection:`Select --> Select/Deselect Last`

These operators will toggle the selection of the first or last control point(s) of the curve(s)
in the object. This is useful to quickly find the start of a curve
(e.g. when using it as path...).


Select Next/Previous
====================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Select Next`, :menuselection:`Select --> Select Previous`

These operators will select the next or previous control point(s),
based on the current selection
(i.e. the control points following or preceding the selected ones along the curve).
In case of a cyclic curve, the first and last points are not considered as neighbors.


Select More/Less
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> More/Less`
   :Hotkey:    :kbd:`Ctrl-NumpadPlus`, :kbd:`Ctrl-NumpadMinus`

Their purpose, based on the currently selected control points, is to reduce or enlarge this selection.

More
   For each selected control point, select *all* its linked points (i.e. one or two...).
Less
   For each selected control point, if *all* points linked to this point are selected, keep this one selected.
   Otherwise, de-select it.

This implies two points:

#. When *all* control points of a curve are selected, nothing will happen
   (as for *Less*, all linked points are always selected, and of course, *More* cannot add any).
   Conversely, the same goes when no control points are selected.
#. Second, these tools will never "go outside" of a curve
   (they will never "jump" to another curve in the same object).
