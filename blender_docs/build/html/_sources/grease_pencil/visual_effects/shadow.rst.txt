.. _bpy.types.ShaderFxShadow:

********************
Shadow Visual Effect
********************

The *Shadow* Visual Effect shows a simulated shadow casting by the object.

For simulating the shadow a color silhouette of the object is displaced in
horizontal and/or vertical direction on the back of the object.


Options
=======

.. figure:: /images/grease-pencil_visual-effects_shadow_panel.png
   :align: right

   Shadow Visual Effect.

Offset
   Control the shadow displacement in pixels on the X and Z axis.

   X, Z

Shadow Color
   Defines the shadow color.

Scale
   Control the size of the shadow on the X and Z axis.

   X, Z

Rotation
   Sets the shadow rotation around the *Grease Pencil* object center
   or another object when *Use Object As Pivot* is enabled.

Blur
   Control the blur scale in pixels on the X and Z axis.

   X, Z

   Samples
      Number of blur samples (0 disabled the blur effect).

Use Object As Pivot
   When enabled, an Object is used by the shadow as the center of rotation.

   Object
      Sets the object to use as the pivot point for the shadow.

Use Wave Effect
   When enabled, apply a wave distortion to the shadow.

   Direction
      Sets horizontal or vertical direction for the waves.

   Amplitude
      Controls the strength and the depth of the wave.

   Period
      Controls the wave period. The time it takes to complete one cycle.

   Phase
      Shifts the wave pattern over the shadow.


Example
=======

.. list-table:: Shadow Effect samples.

   * - .. figure:: /images/grease-pencil_visual-effects_shadow_simple.png
          :width: 200px

          Simple Shadow.

     - .. figure:: /images/grease-pencil_visual-effects_shadow_blur.png
          :width: 200px

          Blurred Shadow.

     - .. figure:: /images/grease-pencil_visual-effects_shadow_stretch.png
          :width: 200px

          Stretched shadow with an Empty as center of rotation.
