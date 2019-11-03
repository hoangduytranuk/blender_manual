.. _bpy.types.SpaceOutliner:
.. _bpy.ops.outliner:

********
Outliner
********

.. figure:: /images/editors_outliner_interface.png
   :align: right

   The Outliner editor.

The *Outliner* is a list that organizes data in the blend-file,
i.e. the scene data, Video Sequencer data, or anything that gets stored in a blend-file.
The *Outliner* can be used to:

- View the data in the scene.
- Select and deselect objects in the scene.
- Hide or show an object in the scene.
- Enable or disable selection (to make an object "unselectable" in the 3D Viewport).
- Enable or disable the rendering of an object.
- Delete objects from the scene.
- Unlink data (equivalent to pressing the *X* button next to the name of a data-block).

.. (TODO) create new objects by drag & drop from the outliner
   drag & drop objects to groups

Each row in the *Outliner* shows a data-block. You can click the plus sign to
the left of a name to expand the current data-block and see what other data-blocks it contains.

You can select data-blocks in the *Outliner*,
but this will not necessarily select the data-block in the scene.
To select the data-block in the scene, you have to activate it.


Selecting and Activating
========================

Single selection does not require any pre-selection: just work directly with :kbd:`LMB`
(and/or the `context menu`_, see below) *inside* the name/icon area.

When you select an object in the list this way,
it is selected and becomes the active object in all other 3D Views.


Selecting a Group of Data-Blocks
--------------------------------

.. figure:: /images/editors_outliner_column-icons.png
   :align: right

   Selection of a data-block.

Useful when you want to select/deselect a whole bunch of data-blocks.
For this you must prepare the selection using, to your liking:

- :kbd:`RMB` or :kbd:`LMB`,
- :kbd:`Shift-RMB` or :kbd:`Shift-LMB`,
- :kbd:`RMB` and drag or :kbd:`LMB` and drag,

all *outside* the name/icon area. Those pre-selected have their line in a lighter color.
You then can (de)select them with an :kbd:`RMB`-click *on* the name/icon area,
which brings on a context menu (see below). :kbd:`A` to select/deselect all open items.


Activating a Data-Block
-----------------------

To "activate" the data-block with :kbd:`LMB` on the *icon* of the data-block.
Activating the data-block will automatically switch to the relevant mode.
For example, activating the mesh data of the cube will select the cube
and enter *Edit Mode* while activating the object data of
the cube will select the cube and enter *Object Mode* (see right).

If the data-block type supports multi-editing,
you can use :kbd:`Shift` to add/remove objects from the edit mode.


.. _editors-outliner-collections:

Collections
===========

Collections are a way Blender uses to organize scenes.
Collections contain objects and everything thing else in a scene.
They can be include collections themselves and are fully recursive.

.. seealso::

   Read more about :doc:`Collections </scene_layout/collections/index>`

New
   Creates a new collection.
Duplicate Collections
   Recursively duplicates the collection including all child collections, objects, and object data.
Duplicate Linked
   Duplicate entire hierarchy keeping content linked with original.
Delete Hierarchy
   Deletes the collection and all of its child objects.
Instance to Scene
   Creates a new :doc:`collection instance </scene_layout/object/properties/instancing/collection>`.
Visibility
   Isolate
      Hides all collections except the selected collection and any parent collections (if any exist).
   Show/Hide
      Shows/Hides the selected collection from the :doc:`View Layer </scene_layout/view_layers/index>`.
   Show/Hide Inside
      Shows/Hides all items that are a member of the selected collection, include child collections,
      from the :doc:`View Layer </scene_layout/view_layers/index>`.
   Enable/Disable in Viewports
      Enables/disables drawing in the :doc:`View Layer </scene_layout/view_layers/index>`.
   Enable/Disable in Renders
      Enables/disables visibility of the collection in renders.
View Layer
   Disable/Enable in View Layer
      Disables/Enables the collection from the view layer.


Context Menu
============

Show the context menu for a data-block with :kbd:`RMB` on the icon or name.
Depending on the type of the pre-selected data-block(s), you will have all or part of the following options:

Copy/Paste
   Copy/pastes selected data-blocks.
Delete
   Deletes the selected data-block.
Select, Select Hierarchy, Deselect
   Add object to current selection without making it the active one.


ID Data Menu
------------

Unlink
   To unlink a data-block from its "owner" (e.g. a material from its mesh).
Make Local
   To create a "local" duplicate of this data-block.
Make Single User
   This feature is not yet implemented.
Delete
   Deletes the selected data-block.
Remap Users
   Remap Users of a data-block to another one (of same type of course).
   This means you can e.g. replace all usages of a material or texture by another one.
Copy/Paste
   Copy/pastes selected data-blocks.
Add Fake User, Clear Fake User
   Adds a "dummy" (fake) user so that the selected data-block always gets saved even if it has no users.
   The fake user can be removed with *Clear Fake User*.
Rename :kbd:`Ctrl-LMB`
   Renames the selected data-block.
Select Linked
   Selects the linked data, see :ref:`bpy.ops.object.select_linked` for more information.


View Menu
---------

The view menu is part of the context menu and supported in all the Outliner elements.

Show Active
   Centers the Tree View to selected object :kbd:`Period`.
Show Hierarchy
   To collapse all levels of the tree :kbd:`Home`.
Show/Hide One Level
   Expand one level down in the tree :kbd:`NumpadPlus` and :kbd:`NumpadMinus` to collapse.


.. note::

   Some data-block types will not have a context menu at all!


Restriction Columns
===================

The following toggles, in the right side of the *Outliner* editor,
are available for collections, objects, bones, modifiers and constraints.

By default only the temporary viewport visibility is enabled.
The other options can be enabled in the *Restriction Toggles* option in the Outliner filter.

- Holding :kbd:`Shift` sets or unsets the value to all its child collections or objects.
- Holding :kbd:`Ctrl` isolates the object or collection, so they are the only ones with its value set.

Visibility (eye icon)
   Toggles the visibility of the object in the 3D View.
Enable collection (checkbox)
   Exclude the collection from the view layer.
   This is not really a restriction column. It is shown besides the collection icon.

.. note::

   The following options need to first be enabled in the Outliner filter.

Selectability (mouse cursor icon)
   This is useful for if you have placed something in the scene
   and do not want to accidentally select it when working on something else.
Rendering (camera icon)
   This will still keep the object visible in the scene, but it will be ignored by the renderer.
   Usually used by support objects that help modeling and animation yet do not belong in the final images.
Global Viewport Visibility (screen icon)
   This will still render the object/collection, but it will be ignored by all the viewports.
   Often used for collections with high-poly objects that need to be instanced in other files.
Holdout (collection only)
   Mask out objects in collection from view layer -- *Cycles only*.
Indirect Only (collection only)
   Objects in these collections only contribute to indirect light -- *Cycles only*.


Header
======

Display Mode
------------

The editors header has a select menu that let you filter what the Outliner should show.
It helps to narrow the list of objects so that you can find things quickly and easily.

Scenes
   Shows *everything* the *Outliner* can display (in all scenes, all view layers, etc.).
View Layer
   Shows all the collections and objects in the current view layer.
Sequence
   Lists :doc:`data-block </files/data_blocks>`
   that are used by the :doc:`Sequencer </video_editing/index>`.
Blender File
   Lists all data in the current blend-file.
Data API
   Lists every :doc:`data-block </files/data_blocks>` along with any properties that they might have.
Orphan Data
   Lists :doc:`data-blocks </files/data_blocks>`
   which are unused and/or will be lost when the file is reloaded.
   It includes data-blocks which have only a fake user. You can add/remove Fake User
   by clicking on cross/tick icon in the right side of the Outliner editor.


Searching
---------

You can search the view for data-blocks,
by using Search field in the header of the *Outliner*,
The `Filter`_ menu lets you toggle the following options:

- Case Sensitive Matches Only
- Complete Matches Only


Filter
------

Restriction Toggles
   Set which `Restriction Columns`_ should be visible.
Sort Alphabetically
   Sort the entries alphabetically.

Collections
   List the objects and collections under
   the :doc:`collection hierarchy </scene_layout/collections/index>` of the scene.
   Objects may appear in more than one collection.
Objects
   List of all the objects, respecting the other filter options.
   Disabled only if you need an overview of the collections without the objects.
Object State
   All
      The default option, no restrictions.
   Visible
      List only the objects visible in the viewports.
      The global and temporary visibility settings are taken into considerations.
   Selected
      Lists the object(s) that are currently selected in the 3D View.
      See :doc:`selecting in the 3D View </scene_layout/object/selecting>` for more information.
   Active
      Lists only the active (often last selected) object.
Object Contents
   List materials, modifiers, mesh data, ...
Object Children
   List the object children. If the *Collections* option is enabled,
   you will see the object children even if the children are not in the collection.
   However the Outliner shows them as a dashed line.
Data-Block
   Allows you to filter out certain data-blocks currently present in the scene.


Miscellaneous
-------------

Some options in the header will only show if compatible with the active `Display Mode`_.

New Collection (View Layer)
   Add a new collection inside selected collection.
Filter ID Type (Orphan Data, Blender File)
   Restrict the type of the data-blocks shown in the Outliner.
Keying Sets (Data API)
   Add/Remove selected data to the active :doc:`Keying Set </animation/keyframes/keying_sets>`.
Drivers
   Add/Remove :doc:`Drivers </animation/drivers/index>` to the selected item.
Purge (Orphan Data)
   Remove all unused data-blocks from the file (cannot be undone).


Example
=======

.. figure:: /images/editors_outliner_example.png

   The Outliner with different kinds of data.
