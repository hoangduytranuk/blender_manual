.. _bpy.types.Brush.pose_origin_type:
.. _bpy.types.Brush.pose_offset:
.. _bpy.types.Brush.pose_smooth_iterations:
.. _bpy.types.Brush.pose_ik_segments:
.. _bpy.types.Brush.use_pose_ik_anchored:

****
Pose
****

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Tool:      :menuselection:`Toolbar --> Pose`

This brush is used to pose a model simulating an armature-like deformation.
The pivot point for rotation is calculated automatically based
on the radius of the brush and the topology of the model.
When pressing :kbd:`Ctrl`, the pose brush applies a twist rotation
to the posing segments instead of using the rotation or an IK deformation.
The falloff of the rotation across multiple segments is controlled by the brush falloff curve.

Rotation Origins
   Method to set the rotation origins for the segments of the brush.

   Topology
      Sets the rotation origin automatically using the topology and shape of the mesh as a guide.
   Face Sets
      Creates a pose segment per :ref:`Face Set <sculpting-editing-facesets>`, starting from the active face set.

Pose Origin Offset
   Offset of the pose origin in relation to the brush radius.
   This is useful to manipulate areas with a lot of complex shapes like fingers.

Smooth Iterations
   Controls the smoothness of the falloff of the deformation.

Pose IK Segments
   Controls how many :ref:`IK bones <bone-constraints-inverse-kinematics>`
   are going to be created for posing.

Keep Anchor Point
   Keeps the position of the last segment in the IK chain fixed.
