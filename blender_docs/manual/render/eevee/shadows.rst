
*******
Shadows
*******

Eevee uses Shadow Mapping techniques to properly shadow the light coming directly
from light objects.

A shadow map is a texture that stores the nearest occluder from the light position.
Eevee also filters the shadow maps in order to smooth out the pixelated appearance.


Global Settings
===============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Shadows`

Method
   Select the shadow map type. It changes how shadows are stored and filtered.

   :abbr:`ESM (Exponential Shadow Mapping)`
      They are fast to filter but light leaking may occur near a occluder.
      This can be minimized by increasing the *Exponent* parameter.
      Another issue is the artifacts present at depth discontinuity.
      Unfortunately, there is no workaround for this issue and the only way
      to minimize it is to reduce the *Soft* parameter.

   :abbr:`VSM (Variance Shadow Mapping)`
      Filters nicely and gives smooth shadow map appearance across the whole shadow range.
      However grainy artifacts will be visible when using a low bit depth.
      It is also prone to light leaking when two occluders overlap.
      In this case the shadows can be overdarkened to reduce the leak,
      by using the *Bleed Bias* parameter.
      VSM uses twice as much memory as ESM, and is slower.

Cube Size
   Size of the shadow cubemaps used to shadow Point, Area and Spot lights.
   Higher shadow map size will give higher precision and sharper shadows.

Cascade Size
   Size of one cascade used by *Cascaded Shadow Maps*. This is only for Sun lamps.

High Bitdepth
   This option can help reduce some artifacts due to float imprecision inside the shadow maps.
   This option effectively double the memory usage of shadow maps and will slow down their update.

Soft Shadows
   Randomize the shadow maps origin to create soft shadows. It needs a lot of samples to get rid of the banding.

Light Threshold
   In order to avoid costly setup time, this distance is first computed
   automatically based on a light threshold. The distance is computed
   at the light origin and using the inverse square falloff. The setting
   can be found inside the :menuselection:`Render Settings panel --> Shadow tab`.

   This light threshold does not take the light shape into account and may not
   suit every case. That is why we provide a per-lamp override where you can
   just set the cut off distance
   (:menuselection:`Light Properties Panel --> Light --> Custom Distance`).

   The influence distance is also used as shadow far clip distance, which might affect how shadows looks.
   This influence distance does not concern sun lights that still have a far clip distance.

   .. seealso::

      :doc:`Custom Limit </render/eevee/lamps>`.

.. note::

   The Soft Shadows method is not physically based and will not match Cycles for very large lamps.

.. tip::

   A 512px cubemap is 6 x 512 x 512 pixels in it.
   Tweaking the *Size* parameters can have a big impact on memory consumption and performance.


Lamp Settings
=============

Common Parameters
-----------------

Clip
   Distance from the light object at which the shadow map starts and ends.
   Any object before this distance will not appear to cast shadows.
   *Clip End* will only appear for sun lamps.

Soft
   Size of the filter applied to the shadow map.
   This filter size is independent from the shadow map resolution.
   Higher filter size can have a big impact on performance.
   There is a maximum cap to filter size (in pixels) that depends on shadow resolution.

Bias
   Bias applied to the depth test to reduce self shadowing artifacts.

Exponent
   Exponent applied to ESM to reduce light leaking.

Bleed Bias
   Bias applied to VSM to reduce light leaking.


Contact Shadows
---------------

This type of shadows exists to fix light leaking caused by Bias or shadow map undersampling.
They uses the depth buffer to find occluders (just like Screen Space Reflections).
However, exactly like Screen Space Reflections, they suffer from the same limitations:
unknown object thickness, effect disappearing at screen edges.

.. tip::

   The distance of action of Contact Shadows should remain quite small.
   They are not accurate enough to shadow the entire scene.

Distance
   World space distance in which to search for screen space occluder.

Softness
   Control how soft the contact shadows will be. Contact shadow blurring does not match light's physical size.

Bias
   Bias applied to the ray tracing to reduce self shadowing artifacts.

Thickness
   Pixel thickness used to detect occlusion. Treat any potential occluder to be this thick.


.. _eevee-cascaded-shadow-map:

Cascaded Shadow Map
-------------------

These special kind of shadow maps are used by Sun lights.
This is because they can shadow large scenes by distributing multiple shadow maps over the frustum range.
Each cascade covers a different portion of the view frustum.
Do note that cascade shadow maps are always updated because they are view dependent.
This means they have a high performance impact.

.. note::

   In orthographic view the cascades cover the whole depth range of the camera with an evenly distrubuted
   shadow precision. 

Count
   Number of cascades to use. More cascade means better precision but slower update.

Fade
   Fade transition area between two cascades.
   Higher values means less overall resolution because cascades need to overlap.

Max Distance
   Distance away from the view origin (or camera origin if in camera view) to cover with the cascade.
   If the view far clip distance is lower than Max Distance, the lowest of the two will be used.
   Only works in perspective view.

Distribution
   Puts more resolution towards the near clip plane. Only works in perspective view.


Limitations
===========

- Shadows are not supported on light instances (dupli objects, group instancing).
- Only 128 active lights can be supported by Eevee in a scene.
- Only 8 Shadowed sun lights can be supported at the same time.
