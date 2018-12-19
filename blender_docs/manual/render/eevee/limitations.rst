
***********
Limitations
***********

Eevee's goal is to be an interactive render engines. Some features may not be there yet or
may be impossible to implement into Eevee's architecture without compromising performance.

Here is a rather exhaustive list of all the limitations you can expect while working with Eevee.


Cameras
=======

- Only perspective and orthographic projections are currently supported.


Lights
======

- Shadows are not supported on light instances (dupli objects, group instancing).
- Only 128 active lights can be supported by Eevee in a scene.
- Only 8 Shadowed sun lights can be supported at the same time.
- As of now, lights can only have one color and does not support light node trees.


Light Probes
============

- Eevee only supports up to 128 active Reflection Cubemaps.
- Eevee only supports up to 64 active Irradiance Volumes.
- Eevee only supports up to 16 active Reflection Planes inside the view frustum.


Indirect Lighting
=================

- Volumetrics don't receive light from Irradiance Volumes but does receive world's diffuse lighting.
- Eevee does not support "specular to diffuse" light bounces nor "specular to specular" light bounces.
  All specular lighting is turned off during baking.


Volumetrics
===========

- Only single scattering is supported.
- Volumetrics are rendered only for the Camera "Rays". They don't appear in reflections/refractions and probes.
- Volumetrics don't receive light from Irradiance Volumes but does receive world's diffuse lighting.
- Volumetric shadowing does only work on other volumetrics. They won't cast shadows on solid objects in the scene.
- Volumetric shadowing does only work for volumes inside the view frustum.
- Volumetric lighting does not respect the Lights shapes. They are treated as point lights


Screen Space Reflections
========================

- Only one glossy BSDF can emit screen space reflections.
- The chosen BSDF is currently arbitrary chosen.
- Screen Space Reflections will reflect transparent objects and objects using Screen Space Refraction
  but without accurate positioning due to the one layer depth buffer.


Screen Space Refraction
=======================

- Only one refraction event is correctly modeled.


Ambient Occlusion
=================

- Objects are treated as infinitely thick, producing overshadowing if the Distance is really large.


Materials
=========

Refraction
   Refraction is faked by sampling the same reflection probe used by the Glossy BSDFs,
   but using the refracted view direction instead of the reflected view direction.
   Only the first refraction event is modeled correctly.
   An approximation of the second refraction event can be used for relatively thin objects using Refraction Depth.

Bump
   As of now, bump mapping is supported using OpenGL derivatives which are the same for each block of 2x2 pixels.
   This means the bump output value will appear pixelated.
   It is recommended to use normal mapping instead.

   .. tip::
   
      If you absolutely need to render using Bump nodes, render at twice the target resolution and downscale the final output.

Volumes Objects
   Object volume shaders will affect the whole bounding box of the object.
   The shape of the volume must be adjusted using procedural texturing inside the shader.


Shader Nodes
============

- All BSDF are using approximations to achieve realtime performance
  so there will always be small differences between Cycles and Eevee.
- Some utility nodes are not yet compatible with Eevee (i.e. Sky Texture node).

.. seealso::

   For a full list of unsupported nodes see :doc:`Nodes Support </render/eevee/materials/nodes_support>`.


Memory Management
=================

As of now Eevee uses OpenGL, and
:abbr:`GPU (Graphic Processing Unit, also known as Graphics Card)` Memory management is done by the OpenGL driver.
In theory, only the needed textures and meshes (now referred as "the resources") for a single draw call (i.e. one object)
needs to fit into the GPU memory.

So if the scene is really heavy, the driver will swap things in and out to make sure all objects are rendered correctly.

In practice, using too much GPU memory can make the GPU driver crash, freeze, or kill the application.
So be careful of what you ask.

There is no standard way of estimating if the resources will fit into the GPU memory and or
if the GPU will render them successfully.


CPU Rendering
=============

Being an OpenGL engine, Eevee only uses the power of
the :abbr:`GPU (Graphic Processing Unit, also known as Graphics Card)` to render.
There is no plan to support :abbr:`CPU (Central Processing Unit)` (software) rendering as it would be very inefficient.
CPU power is still needed to handle high complexity scene as the geometry
is still being prepared by the CPU before rendering each frame.


Multiple GPU Support
====================

There is currently no support for multiple :abbr:`GPU (Graphic Processing Unit, also known as Graphics Card)` system.


Headless Rendering
==================

There is currently no support for using Eevee on headless systems (i.e. without a Display Manager).
