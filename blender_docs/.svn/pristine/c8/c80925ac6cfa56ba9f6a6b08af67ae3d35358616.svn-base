
************
Introduction
************

Eevee's materials system uses the same node based approach as :doc:`Cycles </render/cycles/materials/index>`.


Nodes Support
=============

Due to realtime constraints, not all Cycles features are available in Eevee.
See :doc:`/render/eevee/materials/nodes_support`.


Performance
===========

Performance is highly dependent on the number of BSDF nodes present in the node tree.

.. tip::

   Prefer using the Principled BSDF instead of multiple BSDF nodes because Eevee is optimized for it.


Limitations
===========

Refraction
   Refraction is faked by sampling the same reflection probe used by the Glossy BSDFs,
   but using the refracted view direction instead of the reflected view direction.
   Only the first refraction event is modeled correctly.
   An approximation of the second refraction event can be used for relatively thin objects using Refraction Depth.
   Using Screen Space refraction will refract what is visible in.

Bump
   As of now, Bump mapping is supported using OpenGL derivatives which are the same for each block of 2x2 pixels.
   This means the bump output value will appear pixelated.
   It is recommended to use Normal mapping instead.

   .. note::

      If you absolutely need to render using Bump nodes,
      render at twice the target resolution and downscale the final output.

Volumes Objects
   Object volume shaders will affect the whole bounding box of the object.
   The shape of the volume must be adjusted using procedural texturing inside the shader.
