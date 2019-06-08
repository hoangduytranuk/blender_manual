.. |material-icon| image:: /images/editors_node-editor_introduction_icons-material.png
   :width: 1.0em

********************
Assigning a Material
********************

Materials available in the currently open blend-file can be investigated by clicking
on the Materials icon |material-icon| in the Properties editor Header.
In this section we look at how to assign or remove a material to/from the Active Object in Blender, either by:

- Creating a new material,
- re-using an existing material, or
- deleting a material.

We also give hints about practical material usage.


.. _bpy.ops.material.new:

Creating a new Material
=======================

Every time a new Object is created it has no material linked to it.
You can create a new material for the object by:

- Selecting the object.
- In the Properties editor, click on the object button.
- Click on the Materials button in the Properties editor header.

The Shading panel then appears. This contains the following elements:

.. figure:: /images/render_blender-render_materials_assigning-a-material_creating.png

   Add new material.

- Context: The currently selected scene and object.
- Object Material Slots: this panel shows the "slots"
  for the material (or materials) that this object data contains.
- Active Material: Initially empty, asking for "New".

To add a new material, click "+" in the Active Material box.
This action has a series of effects:

.. figure:: /images/render_blender-render_materials_assigning-a-material_panel-object-mode.png

   Materials Panel with New Entry.

#. Opens the new material in the Active Material box.
#. Brings up additional buttons in the immediate panel.
#. Adds the new material to the Available Materials list.
#. Adds the new material to the Object Material Slots list for the active object (or its object data -- see below).
#. Brings up a :doc:`preview </render/engines/cycles/materials/preview>` of the new material.
#. Provides you with a range of panels allowing you to select
   the :doc:`material settings </render/engines/cycles/materials/settings>` of the new material.


New Material Panel Buttons
--------------------------

Details of the additional buttons which appear in the Material panel for a new Active
Material are as follows:

Active Material
   List View.
Material
   The Material :ref:`Data-Block Menu <ui-data-block>` for the selected Material slot.

.. tip:: Naming materials

   It is a very good idea to give your materials clear names so you can keep track of them,
   especially when they are linked to multiple objects.
   Try to make your names descriptive of the material,
   not its function (e.g. "Yellow Painted" rather than "Kitchen Table Color").

Node
   Use Nodes.
Data
   Specifies whether the material is to be linked to the Object or to the Object Data.
Material type
   This menu has four options which define how the object is to be rendered.


Reusing Existing Materials
==========================

Blender is built to allow you to reuse *anything*, including material settings,
between many objects. Instead of creating duplicate materials,
you can simply reuse an existing material.
There are several ways to do this using the Material's data-block menu:

*Single Object* -- With the object selected, click the sphere located to the left of the Material name.
A pop-up appears showing all the materials available in the current blend-file.
To use one, just click on it.

.. figure:: /images/render_blender-render_materials_assigning-a-material_select-exist-button.png

   Select an existing material.

.. tip:: Searching for Materials

   The search field at the bottom of the material list allows you to search the names in the list.
   For example, by entering "wood" all existent materials are filtered so that
   only materials containing "wood" are displayed in the list.

*Multiple Objects* -- In the 3D View, with :kbd:`Ctrl-L`
you can quickly link all selected objects to the material (and other aspects)
of the :ref:`active object <object-active>`.
Very useful if you need to set a large number of objects to the same material;
just select all of them,
then the object that has the desired material, and :kbd:`Ctrl-L` links them to that "parent".
(See Tip on Linking Data in Creating about data linking).


Deleting a Material
===================

To delete a material, select the material and click X in the Available Materials List entry.

Although the material will seem to disappear immediately,
the Delete action can depend on how the material is used elsewhere.

If the material is linked to the Object and there are other objects which use this material,
then the material will be removed from that object (but remain on all its other objects).

If the "Fake User" button (F) has been lit in the Available Materials list,
then the material will be retained when the file is saved, even if it has no users.

Only if it has 0 "real" users, and no "Fake" user, will the material be permanently deleted.
Note that it will still remain in the Materials list until the blend-file is saved,
but will have disappeared when the file is reloaded.


.. _bi-multiple-materials:

Multiple Materials
==================

Normally,
different colors or patterns on an object are achieved by adding textures to your materials.
However, in some applications you can obtain multiple colors on an object by assigning
different materials to the individual faces of the object.

.. figure:: /images/render_blender-render_materials_assigning-a-material_creating.png

   Add new material.

To apply several materials to different faces of the same object,
you use the Material Slots options in the Materials header panel.

.. figure:: /images/render_blender-render_materials_assigning-a-material_panel-edit-mode.png

   Material menu in edit mode.

The workflow for applying a second material to some faces of an object covered by a base
material is as follows:

#. In Object Mode, apply the base material to the whole object.
#. Create/select the second material (the whole object will change to this new material).
#. In the Active Material box, re-select the base material.
#. Go to Edit Mode and Face Select (a new box appears above the Active Material box with Assign/Select/Deselect).
#. Select the face/faces to be colored with the second material.
#. In the Object Material Slots box, click the :kbd:`Plus` to create a new slot, and while this is still active,
   click on the second material in the Available Materials list.
#. Click the Assign button, and the second material will appear on the selected object faces.

You can also make this new material a copy of an existing material by adding the data-block:

Select the object, get the material, :kbd:`RMB` and Copy data to clipboard.
When you have renamed the material, click "Link: Data" to link to the existing material.
Proceed to assign faces as required.
NB: If you change the material on the original object, the new object color changes too.
