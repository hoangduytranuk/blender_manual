.. _bpy.types.Library:

****************
Linked Libraries
****************

These functions help you reuse materials, objects and other :doc:`data-blocks </data_system/data_blocks>`
loaded from an external source blend-file.
You can build libraries of common content and share them across multiple referencing files.


Append and Link
===============

.. admonition:: Reference
   :class: refbox

   :Editor:    Info Editor
   :Mode:      All Modes
   :Menu:      :menuselection:`File --> Append or Link`
   :Hotkey:    :kbd:`Shift-F1` or :kbd:`Ctrl-Alt-O`

*Link* creates a reference to the data in the source file such that
changes made there will be reflected in the referencing file the next time it is reloaded.

Whereas *Append* makes a full copy of the data into your blend.
You can make further edits to your local copy of the data,
but changes in the external source file will not be reflected in the referencing file.

In the :doc:`File Browser </editors/file_browser/introduction>`
navigate to the external source blend-file and select the data-block you want to reuse.


Options
-------

Relative Path
   Available only when linking, see :doc:`relative paths </data_system/files/relative_paths>`.
Select
   Makes the object *Active* after it is loaded.
Active Layer
   The object will be assigned to the visible layers in your scene.
   Otherwise, it is assigned to the same layers it resides on in the source file.
Instance Groups
   This option links the Group to an object, adding it to the active scene.

Fake User
   Sets a :ref:`Fake User <data-system-datablock-fake-user>` for the appended items.
Localize All
   Appends/links all appended data, including those indirectly linked from other libraries.

When you select an Object type, it will be placed in your scene at the cursor.
Many other data types, cameras, curves, and materials for example,
must be linked to an object before they become visible.

Newly added Group types are available in :menuselection:`Add --> Group Instances` in 3D View,
or for Node Tree groups, the same menu in the Node Editor.

Look in the Outliner, with display mode set to *blend-file*, to see all your linked and appended data-blocks.
:kbd:`Ctrl-LMB` on a file name allows you to redirect a link to another file.


.. _object-proxy:
.. _bpy.ops.object.proxy_make:

Proxy Objects
=============

.. admonition:: Reference
   :class: refbox

   :Editor:    3D View
   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Make Proxy...`
   :Hotkey:    :kbd:`Ctrl-Alt-P`

Lets you make changes locally over an object (or group) linked from an external library.
Some types of changes remain restricted, but others can be made locally, depending on the type of object.
Those changes are not sent to the external library.
:kbd:`Ctrl-Alt-P` makes the active linked object into a local proxy, appending "_proxy" to its name.

Used with rigged models, proxy objects, allow specified bone layers to be linked back to the source file
while the remainder of the object and its skeleton are edited locally.
Set the *Protected Layers* in the source file using the Skeleton panel of the Armatures tab.
See :ref:`Armature Layers <armature-layers>`.
The bones in protected layers will have their position restored from the source file
when the referencing file is reloaded.


.. _data-system-linked-libraries-make-link:
.. _bpy.ops.object.make_links:

Make Link
=========

.. admonition:: Reference
   :class: refbox

   :Editor:    3D View
   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Make Link...`
   :Hotkey:    :kbd:`Ctrl-L`

Links objects between scenes or data-blocks of the active object to all selected objects.
In some case (i.e. Object Data, Modifier) the target objects must be of the same type
than the active one or capable of receiving the data.
The existing data-block of which will be unlinked from them.

Objects to Scene
   Lets you create links to the selected objects into a different scene than the current one.
   A scene name must be chosen other than that of the current one.
   The *Link Objects to Scene* Operator panel lets you choose between scenes.

   This makes the same object exist in two different scenes at once,
   including its position and animation data. The object's origin will change its color.
Type
   Data-block type to link.

   Object Data, Materials, Animation Data, Group, DupliGroup, Modifiers, Fonts

   Transfer UV Maps
      The active UV map of the selected objects will be replaced by a copy of the active UV map of the active object.
      If the selected object doesn't have any UV maps, it is created.
      Objects must be of type mesh and must have the same number of faces (matching geometry).

.. seealso::

   :ref:`data-system-datablock-make-single-user` for unlinking data-blocks.


.. _bpy.ops.object.make_local:

Make Local
==========

.. admonition:: Reference
   :class: refbox

   :Editor:    3D View
   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Make Local...`
   :Hotkey:    :kbd:`L`

Makes the selected or all external objects local in the current blend-file.
This makes e.g. the position editable, because its position is defined in its source file.

Type
   Optionally unlinks the object's Object Data and Material Data.

   Selected Objects, + Object Data, + Materials, All (i.e. including all scenes)

.. note::

   Appending data you already have linked will add objects/groups to the scene,
   but will keep them linked (and un-editable).

   This is done so existing relationships with linked data remain intact.

.. hint::

   Another way to transform an object locally is with
   the use of :doc:`Dupli-Groups </editors/3dview/object/properties/duplication/dupligroup>`.
   Instead of linking to *Objects* directly, it is often more useful to link in *Groups*,
   which can be assigned to empties and moved, while maintaining the link to the original file.

   It is also useful to be able to add/remove objects from the group
   without having to manage linking in multiple objects.


Known Limitations
=================

For the most part linking data will work as expected, however,
there are some corner cases which are not supported.


Circular Dependencies
---------------------

In general, dependencies should not go in both directions.

Attempting to link or append data which links back to the current file will likely result in missing links.


Object Rigid Body Constraints
-----------------------------

When linking objects *directly* into a blend-file, the *Rigid Body* settings
**will not** be linked in since they are associated with their scene's world.

As an alternative, you could link in the entire scene and set it as a :ref:`Background Set <scene-background-set>`.
