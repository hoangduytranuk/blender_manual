
*****
Lamps
*****

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Lamp --> Lamp`

Next to lighting from the background and any object with an emission shader,
lamps are another way to add light into the scene.
The difference is that they are not directly visible in the rendered image,
and can be more easily managed as objects of their own type.


Common Settings
===============

Type
   Defines the physical light shape.

Energy
   Light intensity. Affect both specular and diffuse light. Note: Can be negative but breaks PBR.

Specular
   Specular Light intensity multiplier. Use it for more artistic control.
   Setting this to anything but 1.0 will yield non-photorealistic result.

Size (or Radius)
   Size of the lamp in Blender Units; increasing this will result in softer shadows and shading.

Custom Limit

   If enabled uses *Distance* as the custom attenuation distance instead of global light threshold.
   The *Distance* specify where light influence will be set to 0.

   .. seealso::

      :doc:`Light Threshold </render/eevee/shadows>`.


Lamp Types
==========

Point Lamp
----------

Point lamps emit light equally in all directions.
By setting the *Size* larger than zero, they become spherical lamps,
which give softer shadows (TODO 2.8 link soft shadows) and shading.
The strength of point lamps is specified in Watts.


Spot Lamp
---------

Spot lamps emit light in a particular direction, inside a cone.
By setting the *Size* larger than zero, they can cast softer shadows (TODO 2.8 link soft shadows) and shading.

Spot Shape
   Shape of the area lamp.

   The size parameter defines the size of the cone,
   while the blend parameter can soften the edges of the cone.

.. note::

   Unlike in Cycles the *Size* of the light does not change the softness of the cone.


Area Lamp
---------

Area lamps emit light from a rectangular or elliptic area.

Shape
   Shape of the area lamp.

   Square
      The shape of the lamp can be represented as a square and changed with the *Size* property.
   Rectangle
      The shape of the lamp can be represented as a rectangle and changed with the X and Y values.
   Disk
      The shape of the lamp can be represented as a disk and changed with the *Size* property.
   Ellipse
      The shape of the lamp can be represented as a ellipse and changed with the X and Y values.


Sun Lamp
--------

Sun lamps emit light in a given direction. Their position is not taken into account;
they are always located outside of the scene, infinitely far away,
and will not result in any distance falloff.

However, their position is taken into account for shadowing. See :ref:`eevee-cascaded-shadow-map`.

Because they are not located inside the scene, their strength uses different units,
and should typically be set to lower values than other lights.
