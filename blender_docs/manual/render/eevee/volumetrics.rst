
***********
Volumetrics
***********

Eevee simulate volumetric scattering by evaluating all volume objects inside a the view frustum.

For this it uses several 3D texture which have a high video memory usage.
The textures dimensions can be tweaked using the *Tile Size* and *Samples* parameters.

Object volumes have some limitations (link).

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Volumetrics`

Start
   Start distance of the volumetric effect.

End
   End distance of the volumetric effect.

Tile Size
   Control the quality of the volumetric effects. Lower size increase video memory usage and quality.
   This is the size in pixels, of a volumetric cell.

Samples
   Number of samples to compute volumetric effects. Higher count increase video memory usage and quality.
   These samples are distributed along the view depth (view Z axis).

Distribution
   Blend between linear and exponential sample distribution. Higher values puts more samples near the camera.


Volumetric Lighting
===================

Let the volume scattering scatter light in the scene.
Unnecessary if no Volume Scatter is present in the scene.

Light Clamping
   Clamp light contribution to the volume scattering effect. Reduce flickering and noise.
   Set to 0.0 to disable the clamping.


Volumetric Shadows
==================

Approximate light absorption of the surrounding volume objects. This makes the volumes more opaque to light.
This is a very expensive option and have limitations (link).

Shadow Samples
   Number of samples to compute volumetric shadowing.


Limitations
===========

- Only single scattering is supported.
- Volumetrics are rendered only for the camera "rays". They don't appear in reflections/refractions and probes.
- Volumetrics don't receive Light from light grids but does receive from the world probe.
- Volumetric shadowing does only work on other volumetrics.
- Volumetric shadowing does only work for volumes inside the view frustum.
- Volumetric lighting does not respect the lights shapes. They are treated as point lights.
