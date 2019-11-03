.. _bpy.types.CopyRotationConstraint:

************************
Copy Rotation Constraint
************************

The *Copy Rotation* constraint forces its owner to match the rotation of its target.


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_transform_copy-rotation_panel.png

      Copy Rotation panel.

Target
   :ref:`ui-data-id` used to select the constraints target, and is not functional (red state) when it has none.

Order
   Allows specifying which :term:`Euler` order to use during the copy operation.
   Defaults to the order of the owner.

X, Y, Z
   These buttons control which axes are constrained.

   Invert
      The *Invert* buttons invert their respective rotation values.

Mix
   Specifies how the new rotation is combined with the existing rotation.

   Replace
      The new axis values replace existing values.
   Add
      The new axis values are added to the existing values.
   Before Original
      The new rotation is added before the existing rotation, as if it was applied to
      a parent of the constraint owner.
   After Original
      The new rotation is added after the existing rotation, as if it was applied to
      a child of the constraint owner.
   Offset (Legacy)
      This replicates the behavior of the original Offset checkbox. It was intended
      to be similar to the *Before Original* behavior, but does not work correctly
      with multiple axis rotations, and is thus deprecated.

Space
   Standard conversion between spaces.

.. vimeo:: 171073854
