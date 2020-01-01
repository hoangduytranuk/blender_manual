.. _bpy.types.CopyTransformsConstraint:

**************************
Copy Transforms Constraint
**************************

The *Copy Transforms* constraint forces its owner to have the same transforms as its target.


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_transform_copy-transforms_panel.png

      Copy Transforms panel.

Target
   :ref:`ui-data-id` used to select the constraints target, and is not functional (red state) when it has none.
Mix
   Specifies how the copied transformation is combined with the existing transformation.

   Replace
      The new transformation replaces the existing transformation.
   Before Original
      The new transformation is added before the existing transformation, as if it was
      applied to an imaginary parent of the constraint owner. Scale is handled like in
      the :ref:`Aligned Inherit Scale <bone-relations-inherit-settings>` mode of bones
      to avoid creating shear.
   After Original
      The new transformation is added after the existing transformation, as if it was
      applied locally to an imaginary child of the constraint owner. Scale is handled like
      in the :ref:`Aligned Inherit Scale <bone-relations-inherit-settings>` mode of bones
      to avoid creating shear.
Space
   Standard conversion between spaces.

.. vimeo:: 171108888
