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

.. figure:: /images/rigging_constraints_transform_copy-scale_panel.png

   Copy Scale panel.

Target
   :ref:`ui-data-id` used to select the constraints target,
   and is not functional (red state) when it has none.

X, Y, Z
   These buttons control along which axes the scale is constrained.

Offset
   When enabled, this control allows the owner to be scaled (using its current transform properties),
   relatively to its target's scale.

Space
   Standard conversion between spaces.

.. vimeo:: 171077617
