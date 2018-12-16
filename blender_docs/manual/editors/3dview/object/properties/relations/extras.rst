.. _bpy.types.Object.use_slow_parent:
.. _bpy.types.Object.slow_parent_offset:
.. _bpy.types.Object.track_axis:
.. _bpy.types.Object.up_axis:
.. _bpy.types.Object.use_extra:

****************
Relations Extras
****************

Tracking Axes
   TODO.

   Applies to *DupliFrame* when parent *Follow* is enabled.
   Applies to *DupliVerts* when *Rotation* is enabled.

   Axis
      Axis that points in the "forward" direction.
   Up Axis
      Axis that points in the "upward" direction.

Show Parent
   Create a delay in the parent relation.

   .. warning::

      This may be unsafe for render farms as it may be invalid after jumping around the timeline.

   Offset
      Delay in the parent offset.

Extra Object Update
   Refresh the object again on frame changes.
Extra Data Update
   Refresh the object's data again on frame changes.
