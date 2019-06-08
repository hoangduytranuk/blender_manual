
************
Introduction
************

Selection determines which elements will be the target of our actions.
Selections work on the current scene visible objects.
Blender has advanced selection methods. Both in *Object Mode* and in *Edit Mode*.


.. _object-active:

Selections and the Active Object
================================

Blender distinguishes between two different states of selection:

.. figure:: /images/editors_3dview_object_selecting_introduction_color.png

   Unselected object in black, selected object in orange, and active object in yellow.

In *Object Mode* the last (de)selected item is called the "Active Object"
and is outlined in yellow (the others are orange).
There is exactly one active object at any time (even when nothing is selected).

Many actions in Blender use the active object as a reference (for example linking operations).
If you already have a selection and need to make a different object the active one,
simply re-select it with :kbd:`Shift-RMB`.

All other selected objects are just selected. You can select any number of objects.
In order to change a property or to perform an operation on all selected objects (bones, and sequencer-strips)
hold :kbd:`Alt`, while confirming.
