
*********************
Subsurface Scattering
*********************

This effect mimic real subsurface scattering by blurring the diffuse lighting in screen space.

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Subsurface Scattering`

Samples
   Number of samples to compute the scattering effect.

Jitter Threshold
   For the effect to be efficient, samples needs to be coherent and not random.
   This can lead to cross shaped pattern when the scattering radius is high.
   Increasing the Jitter Threshold will rotate the samples below
   this radius percentage in a random pattern in order to hide the visible pattern.
   This affects performance if the scattering radius is large.

Separate Albedo
   Output the albedo of a BSSRDF in a separate buffer in order to not blur it.
   The *Texture Blur* parameter require this option to be enable to work correctly.
   This option increases the video memory usage but does not have a big impact on performance.


Subsurface Translucency
=======================

The Subsurface Translucency option needs to be enabled in order to make the light go through an object
(like simulating a human ear lit from behind).

- This option does only work if *Subsurface Scattering* is enabled.
- This option only works with shadowed light and does not work with indirect lighting.
