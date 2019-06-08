
*****
Tools
*****

Point Selection
===============

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Hotkey:    :kbd:`RMB` and :kbd:`Shift-RMB`

The simplest form of object selection consists of using :kbd:`RMB` on it.
To add to the selection, use :kbd:`Shift-RMB` on more objects.
If the objects are overlapping in the view, you can use :kbd:`Alt-RMB`
to cycle through possible choices (*Object Mode* only).
If you want to add to a selection this way then the shortcut becomes :kbd:`Shift-Alt-RMB`.
To activate an object that is already selected, click :kbd:`Shift-RMB` on it.

To *deselect* an active object,
click :kbd:`Shift-RMB` one time and hence, two clicks if the object is not active.
Note that this only works if there are no other objects under the mouse.
Otherwise it just adds those to the selection. There appears to be no workaround for this bug.

Also you can use :kbd:`Ctrl-RMB` and :kbd:`Shift-Ctrl-RMB` shortcut
to select the object by its center point rather than its contents.


.. _bpy.ops.view3d.select_border:

Border Select
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Menu:      :menuselection:`Select --> Border Select`
   :Hotkey:    :kbd:`B`

To activate the tool, press :kbd:`B`.
With *Border Select* you draw a rectangle while holding down :kbd:`LMB`.
Any object that lies even partially within this rectangle becomes selected.
If any object that was last active appears in the selection it will become active.

For deselecting objects, use :kbd:`MMB` or *Border Select* again while holding
:kbd:`Shift` or :kbd:`Alt`. To cancel the selection use :kbd:`RMB`.

.. hint::

   *Border Select* adds to the previous selection, so in order to select
   only the contents of the rectangle, deselect all with :kbd:`A` first.


.. _bpy.ops.view3d.select_circle:

Circle Select
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Menu:      :menuselection:`Select --> Circle Select`
   :Hotkey:    :kbd:`C`

*Circle Select* :kbd:`C` is used by moving with dotted circle through objects with :kbd:`LMB`.
You can select any object by touching of circle area.
It is possible to dynamically change the diameter of circle by scrolling :kbd:`Wheel`
or with :kbd:`NumpadPlus` and :kbd:`NumpadMinus` as seen in pictures below.
Deselection is under the same principle -- :kbd:`MMB`.
To cancel the selection use :kbd:`RMB` or key :kbd:`Esc` or :kbd:`Return`.


.. _bpy.ops.view3d.select_lasso:

Lasso Select
============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Hotkey:    :kbd:`Ctrl-LMB`

Lasso select is used by drawing a dotted line around vertices or the origin of the objects,
in *Object Mode*. To use this hold :kbd:`Ctrl-LMB` and simply draw around the points you want to select.

Lasso select adds to the previous selection. For deselection, use :kbd:`Shift-Ctrl-LMB`.


.. _bpy.ops.object.select_all:

(De)select All
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      :menuselection:`Select --> (De)select All`,
               :menuselection:`Select --> Inverse`
   :Hotkey:    :kbd:`A`

If anything was selected it is first deselected.
Otherwise it toggles between selecting and deselecting every visible object.

Action
   Select, Deselect, Invert, Toggle

   Inverse :kbd:`Ctrl-I`
      Selects all objects that were not selected, while deselecting all those which were.


.. _bpy.ops.object.select_random:

Random
======

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Menu:      :menuselection:`Select --> Random`

Randomly selects unselected objects based on percentage probability on currently active layers.
On selecting the operator a numerical selection box becomes available in the *Tool Shelf*.
It is important to note that the percentage represents the likelihood of an unselected object being
selected and not the percentage amount of objects that will be selected.


.. _bpy.ops.object.select_mirror:

Mirror
======

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      :menuselection:`Select --> Mirror`
   :Hotkey:    :kbd:`Shift-Ctrl-M`

Select the Mirror objects of the selected object,
based on their names, e.g. "sword.L" and "sword.R".


.. _bpy.ops.object.select_by_layer:

Select All by Layer
===================

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Select All by Layer`

.. figure:: /images/editors_3dview_object_selecting_tools_all-by-layer.png
   :align: right

   All by Layer selection menu.

This option allows the selection of every single object that belongs to a given layer.
Selected objects become visible.

Match
   The match type for selection.
Extend
   Enable to add objects to current selection rather than replacing the current selection.
Layer
   The layer on which the objects are.

.. tip:: Selection of Objects

   Rather than using the :menuselection:`Select All by Layer` option,
   it might be more efficient to make the needed layers visible and use :kbd:`A` on them.
   This method also allows objects to be deselected.


.. _bpy.ops.object.select_by_type:

Select All by Type
==================

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Select All by Type`

With this tool, it becomes possible to select objects of a certain type in one go.

The types are Mesh, Curve, Surface, Meta, Font,
Armature, Lattice, Empty, Camera, Lamp, Speaker.


.. _bpy.ops.object.select_camera:

Select Camera
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Select Camera`

Selects the active camera, this can be used in a complicated scene to easily find the active camera.


.. _bpy.ops.object.select_more:
.. _bpy.ops.object.select_less:
.. _bpy.ops.object.select_hierarchy:

Select More/Less
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> More/Less`
   :Hotkey:    :kbd:`Ctrl-NumpadPlus`, :kbd:`Ctrl-NumpadMinus`

Their purpose, based on the hierarchical.

More
   Expand the selection to the immediate parent and children of the selected objects.
Less
   Contrast the selection, deselect objects at the boundaries of parent/child relationships.
Parent
   Deselects the currently selected objects and selects their immediate parents.
Child
   Deselects the currently selected objects and selects their immediate children.
Extend Parent
   Extends the selection to the immediate parents of the currently selected objects.
Extend Child
   Extends the selection to the immediate children of the currently selected objects.


.. _bpy.ops.object.select_grouped:

Select Grouped
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Grouped`
   :Hotkey:    :kbd:`Shift-G`

There are two ways to organize the objects in relation to one another.
The first one is *parenting*, and the second is simple *grouping*.
These relationships to an artist's advantage by selecting members of respective families or groups.
*Select Grouped* uses the active object as a basis to select all others.

Children
   Selects all hierarchical descendants of the active object.
Immediate Children
   Selects all direct children of the active object.
Parent
   Selects the parent of this object if it has one.
Siblings
   Select objects that have the same parent as the active object.
   This can also be used to select all root level objects (objects with no parents).
Type
   Select objects that are the same type as the active one.
Layer
   Objects that have at least one shared layer.
Group
   Objects that are part of a group (rendered green with the default theme)
   will be selected if they are in one of the groups that the active object is in.
   If the active object belongs to more than one group,
   a list will pop up so that you can choose which group to select.
Object Hooks
   Every hook that belongs to the active object.
Pass
   Select objects assigned to the same :ref:`render pass <render-cycles-passes>`.
Color
   Select objects with same :ref:`Object Color <objects-display-object-color>`.
Keying Set
   Select objects included in the active :doc:`Keying Set </animation/keyframes/keying_sets>`.
Lamp Type
   Select matching lamp types.
Pass Index
   Select matching object pass index.


.. _bpy.ops.object.select_linked:

Select Linked
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Linked`
   :Hotkey:    :kbd:`Shift-L`

Selects all objects which share a common data-block with the active object.
*Select Linked* uses the active object as a basis to select all others.

Object Data
   Selects every object that is linked to the same Object Data, i.e.
   the data-block that specifies the type (mesh, curve, etc.) and the build
   (constitutive elements like vertices, control vertices, and where they are in space) of the object.
Material
   Selects every object that is linked to the same material data-block.
Texture
   Selects every object that is linked to the same texture data-block.
Dupligroup
   Selects all objects that use the same *Group* for duplication.
Particle System
   Selects all objects that use the same *Particle System*.
Library
   Selects all objects that are in the same :doc:`Library </files/linked_libraries>`.
Library (Object Data)
   Selects all objects that are in the same :doc:`Library </files/linked_libraries>`
   and limited to *object data*.


.. _bpy.ops.object.select_pattern:

Select Pattern
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Select --> Pattern`

Selects all objects whose name matches a given pattern.
Supported wild-cards: \* matches everything, ? matches any single character,
[abc] matches characters in "abc", and [!abc] match any character not in "abc".
As an example \*house\* matches any name that contains "house",
while floor\* matches any name starting with "floor".

Case Sensitive
   The matching can be chosen to be case sensitive or not.
Extend
   When *Extend* checkbox is checked the selection is extended instead of generating a new one.
