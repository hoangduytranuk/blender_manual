
********
Lighting
********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties --> Lamp`

Next to lighting from the background and any object with an emission shader,
lamps are another way to add light into the scene.
The difference is that they are not directly visible in the rendered image,
and can be more easily managed as objects of their own type.


Common Light Settings
=====================

Specular
   Specular Light intensity multiplier. Use it for more artistic control.
   Setting this to anything but 1.0 will yield non-photorealistic result.
Custom Distance
   If enabled uses *Distance* as the custom attenuation distance instead of global light threshold.

   Distance
      Specifies where light influence will be set to 0.

   .. seealso::

      :doc:`Light Threshold </render/engines/eevee/shadows>`.

.. note::

   The light's *Power*/*Strength* affect both specular and diffuse light.


Lamp Types
==========

Point Lamp
----------

Point lamps emit light equally in all directions.
By setting the *Size* larger than zero, they become spherical lamps,
which give softer shadows (TODO 2.8 link soft shadows) and shading.

.. seealso::

   :doc:`Point Lights </render/lighting/lamps/point>`.


Spot Lamp
---------

Spot lamps emit light in a particular direction, inside a cone.
By setting the *Size* larger than zero, they can cast softer shadows (TODO 2.8 link soft shadows) and shading.

.. note::

   Unlike in Cycles the *Size* of the light does not change the softness of the cone.

.. seealso::

   :doc:`Spot Lights </render/lighting/lamps/spot>`.


Area Lamp
---------

Area lamps emit light from a rectangular or elliptic area.

.. seealso::

   :doc:`Area Lights </render/lighting/lamps/area>`.


Sun Lamp
--------

Sun lamps emit light in a given direction. Their position is not taken into account;
they are always located outside of the scene, infinitely far away,
and will not result in any distance falloff.

However, their position is taken into account for shadowing. See :ref:`eevee-cascaded-shadow-map`.

Because they are not located inside the scene, their strength uses different units,
and should typically be set to lower values than other lights.

.. seealso::

   :doc:`Sun Lights </render/lighting/lamps/sun>`.
