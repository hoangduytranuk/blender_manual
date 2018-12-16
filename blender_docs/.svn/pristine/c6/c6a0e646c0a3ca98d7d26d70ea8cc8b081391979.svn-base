.. _bpy.types.CorrectiveSmoothModifier:

**************************
Corrective Smooth Modifier
**************************

This modifier is used to reduce highly distorted areas of a mesh by smoothing the deformations.

This is typically useful *after* an Armature Modifier,
where distortion around joints may be hard to avoid, even with careful weight painting.

To use this modifier effectively, it is useful to understand the basics of how it works.

Rest State
   Used as a reference to detect highly distorted areas.
   The original vertex locations are used by default.
Smoothing
   Many options for this modifier relate to smoothing which is used internally
   to correct the distorted regions.


Options
=======

.. figure:: /images/modeling_modifiers_deform_corrective-smooth_panel.png

   Corrective Smooth Modifier.

The modifier also uses a *Rest* state, to use as a reference.
Internally this modifier uses smoothing, so some of the options adjust the kind of smoothing.

.. Shares description with ``smooth.rst``

Factor
   The factor to control the smoothing amount.
   Higher values will increase the effect.
   Values outside this range (above 1.0 or below 0.0) distort the mesh.
Repeat
   The number of smoothing iterations.
   Higher values generally improve the quality of the smoothing, but the operation is slowed down.
Smooth Type
   Select the smoothing method used.

   Simple
      This simply relaxes vertices to their connected edges.
   Length Weight
      Uses a method of relaxing that weights by the distance of surrounding vertices.
      This option can give higher quality smoothing in some cases,
      by better preserving the shape of the original form.
Vertex Group
   Use to manually select regions to smooth.
Only Smooth
   This option is included to preview the smoothing used, before correction is applied.
Pin Boundaries
   Prevent boundary vertices from smoothing.
Rest Source
   Select the source for reference vertex positions that defines the undeformed state.

   Original Coordinates
      Use the original input vertex positions.
      This relies on the original mesh having the same number of vertices as the original mesh.
   Bind Coordinates
      Optionally you may bind the modifier to a specific state.
      This requires that there are constructive modifiers such as Subdivision Surface or Mirror
      being applied before this modifier in the stack.


Example
=======

.. list-table:: An example of a rig using bone envelopes and not weight painting.

   * - .. figure:: /images/modeling_modifiers_deform_corrective-smooth_example-pose-before.png
          :width: 350px

          Armature only.

     - .. figure:: /images/modeling_modifiers_deform_corrective-smooth_example-pose-after.png
          :width: 350px

          Armature and corrective smooth.
