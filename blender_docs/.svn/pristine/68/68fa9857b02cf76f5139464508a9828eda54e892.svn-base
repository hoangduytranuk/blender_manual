.. _bpy.types.Group:
.. _bpy.ops.group:

******
Groups
******

There can be many objects in a scene: A typical stage scene consists of furniture, props,
lights, and backdrops.
Blender helps you keep everything organized by allowing you to group like objects together.

.. _fig-view3d-grouped-objects:

.. figure:: /images/editors_3dview_object_properties_relations_groups_cubes.png

   Grouped objects.

Group objects together without any kind of transformation relationship.
Use groups to just logically organize your scene,
or to facilitate one-step appending or linking between files or across scenes.
Objects that are part of a group always shows as light green when selected.
See Fig. :ref:`fig-view3d-grouped-objects`.


Groups Menu
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Groups`
   :Hotkey:    :kbd:`Ctrl-G`, etc.

Creating New Group :kbd:`Ctrl-G`
   Creates a new group and adds the selected object(s) to it.
   The name of the new group can be specified in the *Create New Group* Operator panel.
Removing from Group :kbd:`Ctrl-Alt-G`
   Remove the selected objects from a group.
   If the object belongs to more one group a pop-up lets you select the group and
   an option to remove it from all groups.
Removing from All Groups :kbd:`Shift-Ctrl-Alt-G`
   Remove the selected objects from all group.
Add Selected to Active Group :kbd:`Shift-Ctrl-G`
   Adds the selected objects to the groups to which the active object belongs.
Remove Selected from Active Group :kbd:`Shift-Alt-G`
   Causes the selected objects to be removed from the groups to which the active object belongs.


Groups Panel
============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Object tab --> Groups`

.. figure:: /images/editors_3dview_object_properties_relations_groups_panel-outliner.png

   Group panel and Outliner.

All groups that an object has been assigned to are listed in the Properties editor
:menuselection:`Object tab --> Group panel`.

Add to Group
   Adds the selected objects from a group.
   A pop-up lets you specify the group to add to.
New ``+``
   Creates a new group and adds the selected object(s) to it.
Name
   To rename a group, simply click in the groups name field.
Remove ``X``
   To remove an object from a group,
   find the name of the group from which you wish to remove the object,
   and click the ``X`` to the right of the group name.
Specials
   Unlink Group, Select Group, Set Offset From Cursor
Dupligroup Visibility
   Restricting Group Contents via Layers The cluster of layer buttons attached to each group determines from
   which layers the group objects will be included when duplicated.
   If your group contains objects on layers 10, 11 and 12,
   but you disable the layer 12 button in the group controls, duplicates of that group
   (using the :doc:`Dupligroup </editors/3dview/object/properties/duplication/dupligroup>` feature)
   will only show the portions of the group that reside in layers 10 and 11.
Offset
   Applies a locational offset of the dupli-instanced groups from the original object's origin.

.. seealso:: Appending or Linking Groups

   To append a group from another blend-file,
   consult :doc:`this page </data_system/linked_libraries>`.
   In summary, :menuselection:`File --> Link/Append Link` Select a blend-file and then the group.

.. tip:: Selecting Groups

   Groups can be selected, see :ref:`Select Grouped <bpy.ops.object.select_grouped>` for more information.
