.. _bpy.types.UVProjectModifier:

*******************
UV Project Modifier
*******************

.. figure:: /images/modeling_modifiers_modify_uv-project_example.jpg
   :align: center
   :width: 350px

   Projecting the Blender logo onto Suzanne.

The *UV Project* modifier acts like a slide projector.
It emits a UV map from the negative Z axis of a controller object
(such as an :doc:`empty object </modeling/empties>`),
and applies it to the object as the "light" hits it.

`Download an example <https://wiki.blender.org/wiki/File:Uvproject.blend>`__.


Options
=======

.. figure:: /images/modeling_modifiers_modify_uv-project_panel.png
   :align: right

   The UV Project modifier.

UV Map
   Which UV map to modify. Defaults to the active rendering layer.

Projectors
   Up to ten projector objects are supported.
   Each face will choose the closest and aligned projector with its surface normal.
   Projections emit from the negative Z axis (i.e. straight down a camera or light).
   If the projector is a camera, the projection will adhere to its perspective/orthographic setting.
Objects
   Specify the projector object(s).

Aspect X/Y and Scale X/Y
   These allow simple manipulation of the image. Only apply when a camera is used as projector object.


Usage
=====

General
-------

*UV Project* is great for making spotlights more diverse, and also for creating decals to break up repetition.

Usually, an :doc:`Image Texture node </render/shader_nodes/textures/image>` mapped to the UV map
that the modifier targets is added to the object's material.


..
   Comment: think that is no more relevant for 2.80?
..
   Perspective Cameras
   -------------------
..
   When using perspective cameras or spot lights,
   you will likely want to enable the *UV Project* Material Option
   (available in the materials panel),
   This uses a different UV interpolation to prevent distortion.
..
   .. note::
..
      This option is not yet available for Cycles.
