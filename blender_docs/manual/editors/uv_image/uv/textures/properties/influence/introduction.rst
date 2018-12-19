
************
Introduction
************

Not only can textures affect the color of a material,
they can also affect many of the other properties of a material.
The different aspects of a material that a texture influences are
controlled in the *Influence* panel.

.. note::

   Texture options for *Surface* and *Wire* materials and in some cases also for *Volume* and *Halo* materials.


Surface and Wire Materials
==========================

.. figure:: /images/render_blender-render_textures_properties_influence_introduction_surface.png

   Texture Influence panel for a Surface material.


Diffuse
-------

Intensity
   Amount texture affects diffuse reflectivity.
Color
   Amount texture affects the basic color or RGB value of the material.
Alpha
   Influences the opacity of the material.
   Also use *Z Transparency* for light and if combining multiple channels.
Translucency
   Influences the Translucency amount.


Specular
--------

Intensity
   Amount texture affects specular reflectivity.
Color
   Influences the *Specular* color, the color of the reflections created by the lamps on a glossy material.
Hardness
   Influences the specular hardness amount.
   A DVar of 1 is equivalent to a Hardness of 130, a DVar of 0.5 is equivalent to a Hardness of 65.


Shading
-------

Ambient
   Influences the amount of Ambient light the material receives.
Emit
   Influences the amount of light emitted by the material.
Mirror
   Influences the mirror color. This works with environment maps and ray-traced reflection.
Ray Mirror
   Influences the strength of ray-traced mirror reflection.


Geometry
--------

Normal
   Commonly called bump mapping, this alters the direction of the surface normal.
   This is used to fake surface imperfections or unevenness via bump mapping, or to create reliefs.
Warp
   *Warp* allows textures to influence/distort the texture coordinates of a next texture channel.
   The distortion remains active over all subsequent channels, until a new Warp has been set.
   Setting the factor at zero cancels out the effect.
Displace
   Influences the Displacement of vertices,
   for using :doc:`Displacement Maps </editors/uv_image/uv/textures/properties/influence/displacement>`.


Other Controls
--------------

Bump Mapping
   Settings for bump mapping.

   Method
      Best Quality, Default, Compatible, Original
   Space
      Texture Space, Object Space, View Space


Volume Materials
================

.. figure:: /images/render_blender-render_textures_properties_influence_introduction_volume.png

   Texture Influence panel for Volume material.

Special texture options for *Volume* materials.

Density
   Causes the texture to affect the volume's density.
Emission
   Causes the texture to affect the volume's emission.
Scattering
   Amount the texture affects scattering.
Reflection
   Amount the texture affects brightness of out-scattered light.
Emission Color
   Amount the texture affects emission color.
Transmission
   Amount the texture affects result color after light has been scattered/absorbed.
Reflection Color
   Amount the texture affects color of out-scattered light.


Halo Materials
==============

.. figure:: /images/render_blender-render_textures_properties_influence_introduction_halo.png

   Texture Influence panel for a Halo material.

Special texture options for *Halo* materials.

Size
   Amount the texture affects ray mirror.
Hardness
   Amount the texture affects hardness.
Add
   Amount the texture affects translucency.
