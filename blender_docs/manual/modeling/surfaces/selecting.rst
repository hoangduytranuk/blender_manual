
*********
Selecting
*********

.. figure:: /images/modeling_surfaces_selecting_menu.png
   :align: right

   Select menu.

Surface selection in *Edit Mode* is very similar to
:doc:`NURBS curve selection </modeling/curves/editing/introduction>`.
The basic tools are the same as with :doc:`meshes </modeling/meshes/selecting>`,
so you can select a simple control point with an :kbd:`LMB`\ -click,
add to current selection with :kbd:`Shift-LMB` clicks, :kbd:`B` order-select, and so on.


Cursor Selection
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Hotkey:    :kbd:`LMB`

Clicking on a control point selects it,
using modifier keys you can perform other operations.

Extend/Toggle :kbd:`Shift`
   To add to the selection or de-select when the item is already active.


Select Menu
===========

The *Select* menu (3D View headers) is even simpler than for curves...

All these options have the same meaning and behavior as in
:doc:`Object Mode </scene_layout/object/selecting>`
(and the specificities of *Box Select* in *Edit Mode* have already been discussed
:doc:`here </modeling/meshes/selecting>`).

.. container:: lead

   .. clear


Select Linked
-------------

:kbd:`L`, :kbd:`Ctrl-L` will add to the selection the mouse cursor's nearest control point,
and all the linked ones, i.e. all points belonging to the same surface.


Control Point Row
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> Control Point Row`
   :Hotkey:    :kbd:`Shift-R`

This option works a bit like
:ref:`edge loop selection <modeling-meshes-selecting-edge-loops>` for meshes,
inasmuch it selects a whole :ref:`row <modeling-surfaces-rows-grids>` of control points,
based on the active (the last selected) one. The first time you press :kbd:`Shift-R`,
the V row passing through (containing) the active point will be added to the *current* selection.
If you use again this shortcut, you will toggle between the U and V row of this point,
removing *everything else* from the selection.


More and Less
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Select --> More/Less`
   :Hotkey:    :kbd:`Ctrl-NumpadPlus` / :kbd:`Ctrl-NumpadMinus`

Expand or contract the selection based on current selected control points.

More
   For each selected control point, select **all** its linked points (i.e. two, three or four).
Less
   For each selected control point, if **all** points linked to this point are selected, keep it selected.
   For all other selected control points, deselect them.

This implies two points:

#. First, when **all** control points of a surface are selected, nothing will happen
   (as for *Less*, all linked points are always selected, and of course, *More* cannot add any).
   Conversely, the same goes when no control point is selected.
#. Second, these tools will never "go outside" of a surface
   (they will never "jump" to another surface in the same object).
