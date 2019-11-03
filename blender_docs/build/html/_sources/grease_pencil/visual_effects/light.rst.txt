.. _bpy.types.ShaderFxLight:

*******************
Light Visual Effect
*******************

The *Light* Visual Effect applies a simulated light source onto the object.
The source of the light can be controlled and animated by another object.

This fake light source does not cast shadows.

.. note::

   *Grease Pencil* objects are still not affected by real lights objects,
   so this effect can act as workaround to obtain a similar lighting condition
   when in the scene are *Grease Pencil* objects together with 3D meshes and lights.


Options
=======

.. figure:: /images/grease-pencil_visual-effects_light_panel.png
   :align: right

   Light Visual Effect.

Object
   Sets the object to use as the location of the light source.

Energy
   Strength of the source light.
   Higher values increase the intensity of the light.

Ambient
   Strength of the ambient light.


Example
=======

.. list-table:: Light visual effect sample.

   * - .. figure:: /images/grease-pencil_visual-effects_light_original.png
          :width: 320px

          Original Model.

     - .. figure:: /images/grease-pencil_visual-effects_light_sample.png
          :width: 320px

          Empty on top-left used as source light.
