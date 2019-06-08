
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
   Defines the physical light shape. There are several
   :doc:`Types of lights </render/lighting/index>`
   they all share all or some of the options listed below.
Color
   The color of the light source's illumination.
Power/Strength
   Each light type has its own way to control the intensity of the light.

   .. note::

      While this value can be negative, it will break the rules for conservation of energy
      and will no longer be physically based (PBR).
Radius/Size/Angle
   Each light type has some way to control the physical size of the virtual light;
   increasing this will result in softer shadows and shading.
