.. _bpy.types.ID:
.. _bpy.types.BlendData:

***********
Data-Blocks
***********

The base unit for any Blender project is the data-block. Examples of data-blocks include:
meshes, objects, materials, textures, node trees, scenes, texts, brushes, and even screens.

Data-blocks are low level program representations for items inside
Blender. When you consider Blender items at a low level, they are all
Data-blocks, which have common Data-block properties. Data-block level
is needed to handle items in Blender program. However, when
considering a higher level, which is typically visible to users,
Blender items are represented as meshes, objects, materials, textures
etc. which are different things. Data-block level handles the same
high level items (meshes, objects, materials, textures etc.), but only
considers their low level common properties and functions.

For clarity, bones, sequence strips and vertex groups are **not** data-blocks,
they belong to armature, scene and mesh types respectively.

Some common characteristics:

- They are the primary contents of the blend-file.
- They can link to each other, for reuse and instancing.
  (child/parent, object/object-data, with modifiers and constraints too).
- Their names are unique.
- They can be added/removed/edited/duplicated.
- They can be linked between files (only enabled for a limited set of data-blocks).
- They can have their own animation data.
- They can have :doc:`Custom Properties </files/custom_properties>`.

When doing more complex projects, managing data-blocks becomes more important,
especially when inter-linking blend-files.

.. figure:: /images/data-system_data-blocks_view.png

   Data-blocks view.


Users (Garbage Collection)
==========================

It is good to be aware of how Blender
handles data-blocks lifetime, when they are freed and why.

Blender follows the general rule where unused data is eventually removed.

Since it is common to add and remove a lot of data while working,
this has the advantage of not having to manually manage every single data-block.

This works by skipping zero user data-blocks when writing blend-files.

In some cases, you want to save a data-block even when it is unused
(typically for re-usable asset libraries). See `Fake User`_.


.. _data-system-datablock-fake-user:

Fake User
---------

Since zero user data-blocks are not saved,
there are times when you want to force the data to be kept irrespective of its users.

If you are building a blend-file to serve as a library of things that you intend to link to and from other files,
you will need to make sure that they do not accidentally get deleted from the library file.

Do this by giving the data-blocks a *Fake User*, by pressing the *F* button next to the name of the data-block.
This prevents the user count from ever becoming zero: therefore, the data-block will not be deleted
(since Blender does not keep track of how many other files link to this one).


Users (Sharing)
===============

Many data-blocks can be shared among other data-blocks.

Examples where sharing data is common:

- Sharing textures among materials.
- Sharing meshes between objects (instances).
- Sharing animated actions between objects,
  for example to make all the lights dim together.

You can also share data-blocks between files, see:

- :doc:`linked libraries </files/linked_libraries>`.


.. _data-system-datablock-make-single-user:
.. _bpy.ops.object.make_single_user:

Make Single User
================

.. admonition:: Reference
   :class: refbox

   :Editor:    3D View
   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Make Single User`
   :Hotkey:    :kbd:`U`

Makes the selected or all objects data-blocks a single user, that is,
not shared (linked) between other objects than the current one.

Type
   These actions work on the selected objects, or on all the objects of the scene.

   All, Selected Objects
Data-blocks
   Lets you, in addition to the menu predefined selection, choose the type of data-blocks individually.

   Object, Object Data, Materials, Textures, Object Animation


Removing Data-Blocks
====================

As covered in `Users (Garbage Collection)`_, data-blocks are typically removed when they are no longer used.

There are some exceptions to this, however.

The following data-blocks can be removed directly: Scene, Text, Group, and Screen.

Other data-blocks such as Groups and Actions can be *Unlinked* from the *Outliner* context menu.

.. tip::

   Some data (images especially) is hard to keep track of,
   especially since image views are counted as users.

   For data-blocks that can be unlinked hold :kbd:`Shift`, while pressing on the *X* button.
   This force clears the user count, so the data-block will be removed on reloading.


.. _data-system-datablock-types:

Data-Block Types
================

.. EDITORS NOTE:
   Mostly we want to avoid long lists of data -- but in this case,
   it is the only comprehensive list of data-blocks, and something which you cannot
   find directly just through looking at the interface.
   ::
   (TODO add) links to related docs for each type.

.. Image source Scene tab --> Active keying set panel --> ID-block (sound replaced).

.. figure:: /images/data-system_data-blocks_id-types.png
   :align: right

   Data-blocks types with their icon.

For reference, here is a table of data-blocks types stored in blend-files.

:Link:
   Library Linking, supports being linked into other blend-files.
:Pack:
   File Packing, supports file contents being packed into the blend-file
   *(not applicable for most data-blocks which have no file reference)*.

.. EDITORS NOTE:
   For each data-block, we have 2 lines.
   1) a terse description.
   2) how its used.
   ::
   Keep these short.

.. container:: lead

   .. clear

.. |tick|  unicode:: U+2713
.. |cross| unicode:: U+2717
.. |none|  unicode:: U+2014

.. list-table::
   :header-rows: 1
   :class: valign
   :widths: 20 5 5 70

   * - Type
     - Link
     - Pack
     - Description
   * - Action
     - |tick|
     - |none|
     - | Stores animation F-Curves.
       | Used as data-block animation data,
       | and the Non-Linear-Editor.
   * - Armature
     - |tick|
     - |none|
     - | Skeleton used to deform meshes.
       | Used as object data & by the Armature Modifier.
   * - Brush
     - |tick|
     - |none|
     - | Used by paint tools.
   * - Camera
     - |tick|
     - |none|
     - | Used as object data.
   * - Curve
     - |tick|
     - |none|
     - | Used by camera, font & surface objects.
   * - Font
     - |tick|
     - |tick|
     - | References font files.
       | Used by Font object-data.
   * - GreasePencil
     - |tick|
     - |none|
     - | 2D/3D sketch data.
       | Used as overlay *helper* info, by the
       | 3D View, Image, Sequencer & Movie Clip editors.
   * - Group
     - |tick|
     - |none|
     - | Reference object's.
       | Used by dupli-groups & often library linking.
   * - Image
     - |tick|
     - |tick|
     - | Image files.
       | Used by textures & shader nodes.
   * - Lamp
     - |tick|
     - |none|
     - | Used as object-data.
   * - Lattice
     - |cross|
     - |none|
     - | Grid based lattice deformation.
       | Used as object data and by the Lattice Modifier.
   * - Library
     - |cross|
     - |tick|
     - | References to external blend-files.
       | Access from the Outliner's blend-file view.
   * - LineStyle
     - |tick|
     - |none|
     - | Used by the FreeStyle renderer.
   * - Mask
     - |tick|
     - |none|
     - | 2D animated mask curves.
       | Used by compositing nodes & sequencer strip.
   * - Material
     - |tick|
     - |none|
     - | Set shading and texturing render properties.
       | Used by objects, meshes & curves.
   * - Mesh
     - |tick|
     - |none|
     - | Geometry vertices/edges/faces.
       | Used as object-data.
   * - MetaBall
     - |tick|
     - |none|
     - | An isosurface in 3D space.
       | Used as object-data.
   * - MovieClip
     - |tick|
     - |cross|
     - | Reference to an image sequence or video file.
       | Used in the Movie Clip editor.
   * - NodeGroup
     - |tick|
     - |none|
     - | Collections of re-usable nodes.
       | Used in the node editors.
   * - Object
     - |tick|
     - |none|
     - | An entity in the scene with location,
       | scale, rotation.
       | Used by scenes & groups.
   * - Particle
     - |tick|
     - |none|
     - | Particle settings.
       | Used by particle systems.
   * - Palette
     - |tick|
     - |none|
     - | Store color presets.
       | Access from the paint tools.
   * - Scene
     - |tick|
     - |none|
     - | Primary store of all data displayed and animated.
       | Used as top-level storage for objects & animation.
   * - Screen
     - |cross|
     - |none|
     - | Screen layout.
       | Used by each window, which has its own screen.
   * - ShapeKeys
     - |cross|
     - |none|
     - | Geometry shape storage, which can be animated.
       | Used by mesh, curve, and lattice objects.
   * - Sounds
     - |tick|
     - |tick|
     - | References to sound files.
       | Used by speaker objects.
   * - Speaker
     - |tick|
     - |none|
     - | Sound sources for a 3D scene.
       | Used as object-data.
   * - Text
     - |tick|
     - |cross|
     - | Text data.
       | Used by Python scripts and OSL shaders.
   * - Texture
     - |tick|
     - |none|
     - | 2D/3D textures.
       | Used by materials, world and brushes.
   * - World
     - |tick|
     - |none|
     - | Used by scenes for render environment settings.
   * - WindowManager
     - |cross|
     - |none|
     - | The overarching manager for all of Blender's UI;
         this includes screens, notification system, operators, and keymaps.
