.. _bpy.types.SplineIKConstraint:

********************
Spline IK Constraint
********************

The *Spline IK* constraint aligns a chain of bones along a curve.
By leveraging the ease and flexibility of achieving aesthetically
pleasing shapes offered by curves and the predictability and well-integrated
control offered by bones, *Spline IK* is an invaluable tool in the riggers' toolbox.
It is particularly well suited for rigging flexible body parts such as tails, tentacles,
and spines, as well as inorganic items such as ropes.

To set up *Spline IK*, it is necessary to have a chain of
connected bones and a curve to constrain these bones to:

- With the last bone in the chain selected,
  add a *Spline IK* constraint from the *Bone Constraints* tab in the *Properties Editor*.
- Set the 'Chain Length' setting to the number of bones in the chain
  (starting from and including the selected bone)
  that should be influenced by the curve.
- Finally, set *Target* to the curve that should control the curve.


Options
=======

.. figure:: /images/rigging_constraints_tracking_spline-ik_panel.png

   Spline IK panel.

Target
   :ref:`ui-data-id` used to select the target curve.


Spline Fitting
--------------

Chain Length
   How many bones are included in the chain.
Even Division
   Ignore the relative length of the bones when fitting to the curve.
Chain Offset
   Offset the entire chain relative to the root joint.


Chain Scaling
-------------

Y Stretch
   Stretch the Y axis of the bones to fit the curve.
Use Curve Radius
   Average radius of the endpoints is used to tweak the X and Z
   scaling of the bones, on top of the X and Z scale mode.
XZ Scale Mode
   Scaling that a bone undergoes to reach its target.

   None
      Do not scale the X and X axes.
   Bone Original
      Use the original scaling of the bones.
   Inverse Scale
      Scale of the X and Z axes is the inverse of the Y scale.
   Volume Preservation
      Similar to the :ref:`Stretch to <constraints-stretch-to-volume-preservation>` constraint.

.. seealso::

   This subject is seen in-depth in the
   :doc:`Armature Posing section </rigging/armatures/posing/bone_constraints/inverse_kinematics/spline_ik>`.

.. vimeo:: 171282278
