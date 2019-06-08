
************
Introduction
************

.. _render-cycles-settings-scene-simplify:
.. _bpy.types.CyclesRenderSettings.texture_limit:
.. _bpy.types.CyclesRenderSettings.use_camera_cull:
.. _bpy.types.CyclesRenderSettings.camera_cull_margin:
.. _bpy.types.CyclesRenderSettings.use_distance_cull:
.. _bpy.types.CyclesRenderSettings.distance_cull_margin:

Simplify
========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Scene --> Simplify`

.. figure:: /images/render_cycles_settings_scene_introduction_simplify.png

Texture Limit
   Automatically scales textures down so that they are no larger than the values chosen.
   This can help reduce computer memory resources when rendering large scenes with huge textures.

Use Camera Cull
   Automatically culls objects based on the camera frustum defined by the *Margin*.
Use Distance Cull
   Automatically culls objects based on their distance from the active camera.
   This is set via the *Distance* property.

.. seealso::

   There are also several non renderer specific settings which
   are documented :ref:`here <data-system-scenes-properties-simplify>`.
