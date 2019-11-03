.. _bpy.types.CopyScaleConstraint:

*********************
Copy Scale Constraint
*********************

The *Copy Scale* constraint forces its owner to have the same scale as its target.

.. note::

   Here we talk of *scale*, not of *size*! Indeed, you can have two objects,
   one much bigger than the other, and yet both of them have the same scale.
   This is also true with bones: in *Pose Mode*,
   they all have a unitary scale when they are in rest position,
   represented by their visible length.


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_transform_copy-scale_panel.png

      Copy Scale panel.

Target
   :ref:`ui-data-id` used to select the constraints target,
   and is not functional (red state) when it has none.

X, Y, Z
   These buttons control along which axes the scale is constrained.

Power
   Allows raising the copied scale to the specified arbitrary power.

Offset
   When enabled, the constraint combines the copied scale with the owner's scale,
   instead of overwriting it.

Additive
   Uses addition instead of multiplication in the implementation of the *Offset* option.

Space
   Standard conversion between spaces.

.. note::

   Since scale is a multiplicative quantity, it should be combined using multiplication,
   and split into fractions or inverted via power. Thus the use of *Power* is
   more mathematically correct than *Influence*, which uses linear interpolation.
   The use of the *Additive* option is also not recommended.

.. vimeo:: 171077617
