
**********
Lamp Panel
**********

.. figure:: /images/render_blender-render_lighting_lights_lamp-panel_panel.png

   Lamp tab.

Lamp
   A :ref:`ui-data-block`. Its list shows all light settings used in the current scene.
Texture Count
   Shows the count of textures in the lamp texture stack.


Preview
=======

A quick preview of the light settings.


Lamp
====

Type
   :doc:`Types of lamps </render/lighting/index>` share all or some of the options listed here:
Color
   The color of the light source's illumination.
Energy
   The intensity of the light source's illumination from (0.0 to 10.0).
Distance
   The *Distance* number button indicates the number of Blender Units (BU)
   at which the intensity of the current light source will be half of its intensity.
   Objects less than the number of BU away from the lamp will get more light,
   while objects further away will receive less light.
   Certain settings and lamp falloff types affect how the *Distance* is interpreted,
   meaning that it will not always react the same.

   The *Sun* and *Hemi* Lamps are another class of Lamps which uses a constant falloff.
   Those lamps do not have a *Distance* parameter, and are often called "Base Lighting Lamps".


.. _bi-lamp-influence:

Influence
---------

Every lamp has a set of switches that control which objects receive its light,
and how it interacts with materials.

Negative
   Let the lamp cast negative light.
   The light produced by the lamp is *subtracted* from the irradiance on the surfaces it hits,
   which darkens these surfaces instead of brightening them.
This Layer Only
   The Lamp only illuminates objects on the same layer the lamp is on.
   Causes the lamp to only light objects on the same layer.
Specular
   The Lamp creates specular highlights.
Diffuse
   The Lamp affects diffuse shading.
