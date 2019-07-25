
.. _bpy.types.ArmatureConstraint:

*******************
Armature Constraint
*******************

*Armature* is the constraint version of the :ref:`Armature Modifier <bpy.types.ArmatureModifier>`,
exactly reproducing the weight-blended bone transformations and applying it to its owner orientation.
It can be used like a variant of the :ref:`Child Of <bpy.types.ChildOfConstraint>` constraint
that can handle multiple parents at once, but requires all of them to be bones.


Target List
===========

.. figure:: /images/animation_constraints_relationship_armature_panel.png

   Armature panel.

This specifies the list of bones used by the constraint to deform its owner.

Add Target Bone
   This button adds a new empty entry at the end of the target list.

Target Entries
   Each target bone has the following input fields and controls:

   Armature
      Unlike the modifier, the constraint can use bones coming from
      different armatures at the same time.

   Bone
      Name of the target bone.

   Remove Button ``-``
      Removes the entry from the target list.

   Blend Weight
      Weight associated with the bone, equivalent to vertex groups in the modifier.

      This value can be animated.

Normalize Weights
   This button normalizes all weight values in the target list so that they add up to 1.0.

.. note::

   Unlike the modifier, the constraint does not take
   the :doc:`Deform </animation/armatures/bones/properties/deform>` checkbox
   of bones into account, and can use any bone as target.


Options
=======

Additional settings of the constraint.

Preserve Volume
   Like the matching option of the modifier, it enables the use of quaternions
   for preserving the volume of the object during deformation.

Use Envelopes
   To approximate envelope-only behavior of the modifier,
   add all relevant bones with weight 1.0 and enable this option.

   .. note::

      Unlike the modifier, the constraint always requires explicitly listing all
      of its target bones with associated weights. This option merely enables
      envelopes for all bones, as if they had :ref:`Envelope Multiply <armature-bones-envelope>` enabled.

Use Current Location
   Only for constraints on bones: Instead of using the rest location,
   use the current location of the owner bone to compute envelope weights or
   binding to B-Bone segments.

   With envelope weights, this can be used to change the active "parent" bone
   of the owner bone dependent on its location. For non-bones this mode is always active,
   because they don't have a rest location.
