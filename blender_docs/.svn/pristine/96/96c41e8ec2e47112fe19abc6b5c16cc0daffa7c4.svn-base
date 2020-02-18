.. _bpy.types.FluidDomainSettings.use_guide:
.. _bpy.types.FluidDomainSettings.guide_alpha:
.. _bpy.types.FluidDomainSettings.guide_beta:
.. _bpy.types.FluidDomainSettings.guide_vel_factor:
.. _bpy.types.FluidDomainSettings.guide_source:
.. _bpy.types.FluidDomainSettings.guide_parent:

******
Guides
******

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Guides`
   :Type:      Domain

Fluid guides are used to apply forces onto the simulation. They are like simple external forces
but also seek to preserve the physically accurate flow of the fluid.
The *Guides* panel allows you to adjust guiding forces globally, i.e. for the entire domain.
Enabling the guides hints the fluid solver to use the more accurate,
but also computationally more expensive pressure solving step.

.. note::

   Even when there are no guiding objects baked or there is no guiding domain attached,
   the fluid solver will still perform the more expensive pressure guiding algorithm
   if guiding is enabled.

Weight
   Controls the lag of the guiding. A larger value (also known as the 'alpha' guiding value)
   results in a greater lag.

Size
   This setting determines the size of the vortices that the guiding produces.
   A greater guiding size (also known as the blur radius or 'beta' guiding value)
   results in larger vortices.

.. youtube:: 92--xX6q7w0

Velocity Factor
   All guiding velocities are multiplied by this factor. That is, every cell of the guiding grid,
   which has the same size as the domain object, is multiplied by this factor.

Velocity Source
   Guiding velocities can either come from objects that move inside the domain
   or from other fluid domains. Former need to be declared as fluid *Effector* objects
   and baked, usually after animating them by hand. Latter can be selected with
   the selection tool but need to be baked already.

   Once effector objects have been baked it is not possible to change the fluid domain resolution anymore.
   When using another fluid domain as the guiding source,
   this domain can have a different resolution and may also be of a different type
   (e.g. the guiding domain is of type *Gas* while the actual domain with the guiding effect
   in it is of type *Liquid*).

Guide parent
   When using *Domain* as the velocity source, this field serves to select the guiding domain object.
