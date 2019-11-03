.. _bpy.types.StretchToConstraint:

*********************
Stretch To Constraint
*********************

The *Stretch To* constraint causes its owner to rotate and scale its Y axis towards its target.
So it has the same tracking behavior as the :doc:`Track To constraint </animation/constraints/tracking/track_to>`.
However, it assumes that the Y axis will be the tracking and stretching axis,
and does not give you the option of using a different one.

It also optionally has some raw volumetric features,
so the owner can squash down as the target moves closer,
or thin out as the target moves farther away.
Note however, that it is not the real volume of the owner which is thus preserved,
but rather the virtual one defined by its scale values. Hence,
this feature works even with non-volumetric objects, like empties, 2D meshes or surfaces,
and curves.

With bones, the "volumetric" variation scales them along their own local axes
(remember that the local Y axis of a bone is aligned with it, from root to tip).


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_tracking_stretch-to_panel.png

      Stretch To panel.

Target
   :ref:`ui-data-id` used to select the constraints target, and is not functional (red state) when it has none.
Rest Length
   This number field sets the rest distance between the owner and its target, i.e.
   the distance at which there is no deformation (stretching) of the owner.

   Reset
      When clicked, this small button will recalculate the *Rest Length* value,
      so that it corresponds to the actual distance between the owner and its target
      (i.e. the distance before this constraint is applied).

.. _constraints-stretch-to-volume-preservation:

Volume Variation
   This number field controls the amount of "volume" variation exponentially to the stretching amount.
   Note that the 0.0 value is not allowed, if you want to disable the volume feature,
   use the *None* button (see below).
Volume Min/Max
   Limits for the volume preservation to a minimum and maximum scaling each by a *Bulge* factor.
Smooth
   Smoothness factor to make limits less visible.
Volume
   These buttons control which of the X and/or Z axes should be affected (scaled up/down)
   to preserve the virtual volume while stretching along the Y axis.
   If you enable the *none* button, the volumetric features are disabled.
Plane
   These buttons are equivalent to the *Up* ones of
   the :doc:`Track To constraint </animation/constraints/tracking/track_to>`:
   they control which of the X or Z axes should be maintained (as much as possible) aligned with the global Z axis,
   while tracking the target with the Y axis.

.. vimeo:: 171283118
