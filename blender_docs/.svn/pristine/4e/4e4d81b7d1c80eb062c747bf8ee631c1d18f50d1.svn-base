
************
Introduction
************

Scenes are a way to organize your work.
Each blend-file can contain multiple scenes, which share other data such as objects and materials.

Scene management and library appending/linking are based on Blender's
:doc:`Library and Data System </data_system/index>`,
so it is a good idea to read that manual page first, if you are not familiar with the basics of that system.

You can select and create scenes with the *Scene data-block* menu in the *Info Editor* header.


Controls
========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Info Editor Header --> Scene`

.. figure:: /images/data-system_scenes_introduction_menu.png
   :align: right

   Scene data-block menu.

Scenes
   A list of available scenes.
Add ``+``
   New
      Creates an empty scene with default values.
   Copy Settings
      Creates an empty scene, but also copies
      the settings from the active scene into the new one.
   Link Objects
      This option creates a new scene with the same settings and contents as the active scene.
      However, instead of copying the objects,
      the new scene contains links to the objects in the old scene.
      Therefore, changes to objects in the new scene will result in the same
      changes to the original scene, because the objects used are literally the same.
      The reverse is also true.
   Link Object Data
      Creates new, duplicate copies of all of the objects in the currently selected scene,
      but each one of those duplicate objects will have links to the object-data (meshes, materials and so on)
      of the corresponding objects in the original scene.

      This means that you can change the position,
      orientation and size of the objects in the new scene without affecting other scenes,
      but any modifications to the object-data (meshes, materials, etc.) will also affect other scenes.
      This is because a single instance of the "object-data" is now being shared by all of the objects
      in all of the scenes, that link to it.
      This has the effect of making a new independent copy of the object-data.
   Full Copy
      Using this option, nothing is shared.
      This option creates a fully independent scene with copies of the active scene's contents.
      Every object in the original scene is duplicated, and a duplicate,
      private copy of its object-data is made as well.

   .. note::

      To choose between these options,
      it is useful to understand the difference between *Object* and *Object Data*.
      See :doc:`Duplication </editors/3dview/object/editing/duplication>`.

      The choices for adding a scene, therefore, determine just how much of this information will be
      *copied from* the active scene to the new one, and how much will be *shared* (linked).

Delete ``X``
   You can delete the current scene by clicking the *X* next to the name in the Info Editor.

.. seealso:: Linking to a Scene

   You can :ref:`link <data-system-linked-libraries-make-link>` any object from one scene to another.
