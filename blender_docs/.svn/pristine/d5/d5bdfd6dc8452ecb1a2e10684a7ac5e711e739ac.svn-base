
********
Surfaces
********

The surface shader defines the light interaction at the surface of the mesh.
One or more :abbr:`BSDF (Bidirectional scattering distribution function)`\ 's specify
if incoming light is reflected back, refracted into the mesh, or absorbed.

Emission defines how light is emitted from the surface,
allowing any surface to become a light source.


Terminology
===========

BSDF
   Stands for Bidirectional Scattering Distribution Function.
   It defines how light is reflected and refracted at a surface.
Reflection
   BSDFs reflect an incoming ray on the same side of the surface.
Transmission
   BSDFs transmit an incoming ray through the surface, leaving on the other side.
Refraction
   BSDFs are a type of *Transmission*, transmitting an incoming ray and
   changing its direction as it exits on the other side of the surface.


BSDF Parameters
===============

A major difference from non-physically-based renderers is that direct light reflection from
lamps and indirect light reflection of other surfaces are not decoupled, but rather handled
using a single :abbr:`BSDF (Bidirectional scattering distribution function)`.
This limits the possibilities a bit, but we believe overall it is helpful in creating
consistent-looking renders with fewer parameters to tune.

Roughness
   For the glossy :abbr:`BSDF (Bidirectional scattering distribution function)`\ s,
   the *roughness* parameter controls the sharpness of the reflection, from 0.0 (perfectly sharp)
   to 1.0 (very soft). Compared to *hardness* or *exponent* parameters,
   it has the advantage of being in the range 0.0 to 1.0,
   and as a result gives more linear control and is more easily textureable.
   The relation is roughly: *roughness* = 1 - 1/*hardness*

   .. note::

      Currently Blender is coded to use an unsquared model.
      So if you are using a :term:`Roughness Map` chances are that the result will not be accurate.
      To fix this, you can square the texture by connecting the texture to
      a :doc:`Math node </render/cycles/nodes/types/converter/math>`
      and either setting it to *Multiply* and inputing the texture in both input sockets,
      or using the *Power* function and setting the second input to 2.
