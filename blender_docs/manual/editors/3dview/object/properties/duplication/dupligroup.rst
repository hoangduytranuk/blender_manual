.. _bpy.types.Object.dupli_group:

**********
DupliGroup
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Object --> Duplication --> Group`

*Duplication Group* or *DupliGroup* allows you to create an instance of a group for each instance of another object.
*DupliGroups* may contain animations, objects with physics simulations and even other nested *DupliGroups*.


Basic Usage
===========

Create a Group:
   - Selecting the objects to be grouped.
   - Create a new group :menuselection:`Object --> Group --> Create New Group`.
   - Rename your group in the Properties editor: :menuselection:`Object --> Groups`.
Create a new Group Instance:
   - :menuselection:`Add --> Group Instance`
Change the Group Instance of existing objects:
   - In the Properties editor: :menuselection:`Object --> Duplication`, enable *Group*.
   - Select the name of your newly created group.

At this point, an instance of the group and an :doc:`empty object </modeling/empties>` will appear.
You can duplicate the empty, and the DupliGroup settings will be preserved for each empty.
This way, you can get multiple copies of linked data very easily.


DupliGroup and Dynamic Linking
==============================

See :doc:`Appending and Linking </data_system/linked_libraries>`
to understand how to dynamically link data from another blend-file into the current file.
You can dynamically link groups from one blend-file to another.
When you do so, the linked group does not appear anywhere in your scene
until you create an object controlling where the group instance appears.

.. important::

   Material Transparency will not display when instancing dupli-groups;
   this is a known limitation of Blender's viewport.


Making a DupliGroup Object Real
===============================

Say you want to make further edits on a DupliGroup instance:
Simply select your DupliGroup and press :kbd:`Shift-Ctrl-A` to convert the DupliGroup
into regular objects that can be transformed and animated normally.

.. note::

   Note that if the DupliGroup was linked from an external file, the Object Data
   (mesh, materials, textures, transforms) will also still be linked from the original group.
   However, the various object's parent-child relationships do not carry over.
