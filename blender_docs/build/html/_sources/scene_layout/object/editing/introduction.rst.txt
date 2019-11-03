
************
Introduction
************

This section describes tools for manipulating objects in Object Mode.
All editing tools can be found in Object menu.


.. _bpy.ops.object.join:
.. _object-join:

Join
====

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Join`
   :Hotkey:    :kbd:`Ctrl-J`

Join merges all selected objects into the last selected *Active* object.
All object data is linked to the active object (which must be selected).
All objects must be of the same type: mesh, curve, surface or armature.
If several curves are joined, each one will keep its subtype (NURBS or Bézier).

.. note::

   Object data has many attributes which may be handled when joining.

   Materials, vertex groups, UV and Vertex layers will be merged.

   Modifiers, constraints, groups and parent relationships are ignored
   when joining and will not be applied to the active object.


.. _object-convert-to:
.. _bpy.ops.object.convert:


Convert To
==========

Curve from Mesh/Text
--------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Convert to --> Curve from Mesh/Text`

Mesh objects and text objects can be converted into curve objects.
In mesh objects, only edges belonging to no faces will be taken into account.
The resulting curve will be a Poly curve type, but can be converted to have
smooth segments as described in :ref:`curve-convert-type`.


Mesh from Curve/Metaball/Surface/Text
-------------------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Convert to --> Mesh from Curve/Meta/Surf/Text`

Converts the selected curve, metaball, surface and text objects to mesh objects.
The actual defined resolution of these objects will be taken into account for the conversion.
Note that it also keeps the faces and volumes created by closed and extruded curves.


Options
-------

Keep Original
   Duplicates the original object before converting it.


.. _object-show-hide:
.. _bpy.ops.object.hide_view:

Show/Hide
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      :menuselection:`Object --> Show/Hide`

Show Hidden Objects :kbd:`Alt-H`
   Reveals all hidden objects.
Hide Selected :kbd:`H`
   Hides all selected objects.
Hide Unselected :kbd:`Shift-H`
   Hides all unselected objects of the scene.


.. _bpy.ops.object.delete:

Delete
======

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Delete`
   :Hotkey:    :kbd:`X` or :kbd:`Delete`

The selected objects are deleted from the scene.

Delete Globally
   Delete the selected objects from all scenes.
