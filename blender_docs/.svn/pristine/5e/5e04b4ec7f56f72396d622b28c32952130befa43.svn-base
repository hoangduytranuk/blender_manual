
*****************
Material Settings
*****************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Material --> Options`


Blend Mode
==========

After calculating the color of a surface, Eevee needs to know how to add it to the color buffer.
Depending on the blend mode the final color will be different.

.. note::

   Additive, Multiplicative and Alpha Blending are considered "Transparent" blend mode.
   This has implications regarding screen space effects.

Opaque
   The previous color will be overwritten by the surface color.
   The alpha component is ignored. This is the fastest option.

Additive
   The surface color will be added to the previous color.
   The alpha value will be used to mix surface color with the neutral color black (0.0, 0.0, 0.0).

Multiplicative
   The previous color will be multiplied by the surface color.
   The alpha value will be used to mix surface color with the neutral color white (1.0, 1.0, 1.0).

Alpha Clip
   The previous color will be overwritten by the surface color,
   but only if the alpha value is above the clip threshold.

Alpha Hashed
   The previous color will be overwritten by the surface color,
   but only if the alpha value is above a random clip threshold.
   This statistical approach is noisy but is able to approximate alpha blending without any sorting problem.
   Increasing the sample count in the render settings will reduce the resulting noise.

Alpha Blending
   Use alpha blending to overlay the surface color on top of the previous color.


Sorting Problem
===============

When writing to the color buffer using transparent blend modes,
the order in which the color blending happens is important as it can change the final output color.
As of now Eevee does not support per-fragment (pixel) sorting or per-triangle sorting.
Only per-object sorting is available and is automatically done on all transparent surfaces based on object origin.

.. note::

   This per-object sorting has already a cost and having thousands of
   these objects in a scene will greatly degrade performance.

Additive and Multiplicative blending are, individually, order independent.
This means all the triangles of a surface rendered with one of these blending mode
will always output the expected result if they do not intersect with other transparent surfaces.
This will work even if the triangles of that surface intersect each others.

However this does not work with Alpha Blending, where even triangle order is important.
In this case you can disable the *Show Backside* option.

Show Backside
   If enabled all transparent fragments will be rendered.
   If disabled, only the frontmost surface fragments will be render.
   Disable this option to ensure correct appearance of transparent from any point of view.


Transparent Shadow
==================

Type of shadows used for this transparent surface.
Eevee does not support colored shadow maps.

Half transparent shadows can be produced by using hashed transparent shadows and larger Soft value on shadow map.

None
   The surface will not cast any shadow.

Opaque
   The surface will cast shadows like an opaque surface.

Clip
   The surface will cast shadows like an opaque surface,
   but only areas where the alpha value is above the clip threshold.

Hashed
   The surface will cast shadows like an opaque surface,
   but only areas where the alpha value is above a random threshold.


Screen Space Refraction
=======================

Enabling Screen Space Refraction on a surface means that refraction BSDFs
will do a raytrace against the depth buffer to find the most accurate refracted color.
This has a big performance cost if the surface covers a lot of pixels.

Screen Space Reflections is not compatible with Screen Space Refraction.
It will be disabled on the surfaces that uses it.
Surfaces that uses Screen Space Refraction will not appear in Screen Space Reflections.

If this option is disabled or if the Screen Space Refraction raytrace fails,
the refracted ray will use the color of the nearest probe.

Screen Space Refraction
   Enable screen space refraction.

Refraction Depth
   If Refraction Depth is not 0.0, all refraction BSDFs in the shader will act as
   if the object would be a thin slab of the refraction material with this thickness.
   This will model a second refraction event that will double the absorption color and
   start the refraction ray after this second event.

   This option greatly increase the quality of thin glass objects.


Subsurface Translucency
=======================

Eevee's Subsurface Scattering algorithm works by blurring the irradiance in screen space.
This means that if no visible part of the surface is lit, the effect disappear.

However, true Subsurface Scattering goes beneath the surface and can travel a lot of distance.
This is why a human ear lit from behind appears red on the front side.

That is what this effect mimics. This translucency approximation does only work
with lamps that have shadow maps and only on Subsurface BSDFs (not the Translucency BSDFs).
It does not work with indirect lighting. The soft parameter of the shadow maps also affects this effect.
