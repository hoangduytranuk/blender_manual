
**************
Light Settings
**************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties --> Light` and :menuselection:`Shader Editor --> Sidebar --> Settings`

Next to lighting from the background and any object with an emission shader,
lights are another way to add light into the scene.
The difference is that they are not directly visible in the rendered image,
and can be more easily managed as objects of their own type.


Common
======

:doc:`Light settings </render/lights/light_object>` for all renderers.


Eevee
=====

Specular
   Specular Light intensity multiplier. Use it for more artistic control.
   Setting this to anything but 1.0 will yield non-photorealistic result.
Custom Distance
   If enabled uses *Distance* as the custom attenuation distance instead of global light threshold.

   Distance
      Specifies where light influence will be set to 0.

   .. seealso::

      :doc:`Light Threshold </render/eevee/render_settings/shadows>`.

.. note::

   The light's *Power*/*Strength* affect both specular and diffuse light.


Shadows
=======

All lights can cast shadows, see :doc:`shadow settings </render/eevee/render_settings/shadows>`.


Limitations
===========

- Unlike in Cycles, the *Size* of spot lights does not change the softness of the cone.
