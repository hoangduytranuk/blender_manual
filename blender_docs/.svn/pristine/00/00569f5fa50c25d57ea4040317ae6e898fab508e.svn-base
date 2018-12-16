
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

.. tip::

   Point, Spot, and Area Lamps also have texture coordinates.


Common Settings
===============

Type
   Currently *Point*, *Spot*, *Area* and *Sun* lamps are supported.
   *Hemi* lamps are not supported, and will be rendered as sun lamps.
Size
   Size of the lamp in Blender Units; increasing this will result in softer shadows and shading.
Samples
   For the branch path tracing integrator, this specifies the number of direct light samples per AA sample.
   Point lamps might need only one sample, while area lamps typically need more.
Max Bounces
   Maximum number of times light from the lamp is allowed to :term:`bounce <light bounces>`.
   Limited by :ref:`scene-wide bounce settings <cycles-bounces>`.
Cast Shadow
   By disabling this option, light from lamps will not be blocked by objects in between.
   This can speed up rendering by not having to trace rays to the light source.
Multiple Importance Sample
   By default lamps use only direct light sampling. For area lights and sharp glossy reflections, however,
   this can be noisy,
   and enabling this option will enable indirect light sampling to be used in addition to reduce noise.


Lamp Types
==========

Point Lamp
----------

Point lamps emit light equally in all directions.
By setting the *Size* larger than zero, they become spherical lamps,
which give softer shadows and shading. The strength of point lamps is specified in Watts.


Spot Lamp
---------

Spot lamps emit light in a particular direction, inside a cone.
By setting the *Size* larger than zero, they can cast softer shadows and shading.
The size parameter defines the size of the cone,
while the blend parameter can soften the edges of the cone.


.. _render-cycles-lamps-area:

Area Lamp
---------

Area lamps emit light from a square or rectangular area with a Lambertian distribution.

Shape
   Shape of the lamp.

   Rectangle
      The shape of the lamp can be represented as a rectangle and changed with the "X" and "Y" values.
   Square
      The shape of the lamp can be represented as a square and changed with the *Size* property.


.. _render-cycles-lamps-area-portals:

Light Portals
^^^^^^^^^^^^^

Area lamps can also function as light portals to help sample the environment light,
and significantly reduce noise in interior scenes.
Note that rendering with portals is usually slower, but as it converges more quickly, less samples are required.

Light portals work by enabling the *Portal* option, and placing areas lamps in
windows, door openings, and any place where light will enter the interior.

In outdoor scenes most rays do not bounce much and just fly off into the sky and therefore,
light portals are not helpful for outdoor scenes.

.. figure:: /images/render_cycles_lamps_portals2.jpg
.. figure:: /images/render_cycles_lamps_portals.jpg

   White Room model by Jay Hardy.


Sun Lamp
--------

Sun lamps emit light in a given direction. Their position is not taken into account;
they are always located outside of the scene, infinitely far away,
and will not result in any distance falloff.

Because they are not located inside the scene, their strength uses different units,
and should typically be set to lower values than other lights.
