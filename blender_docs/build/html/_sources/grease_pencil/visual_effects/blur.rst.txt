.. _bpy.types.ShaderFxBlur:

******************
Blur Visual Effect
******************

The *Blur* Visual Effect applies a Gaussian blur to the object.


Options
=======

.. figure:: /images/grease-pencil_visual-effects_blur_panel.png
   :align: right

   Blur Visual Effect.

Factor
   Control the blur scale in pixels on the X and Z axis.

   X, Z

Samples
   Number of Blur samples (0 disabled the blur effect).

Lock Focal Plane
   When enabled, the blur effect uses the focal plane distance of the actual camera
   to simulate a depth of field effect. Only available in camera view.


Example
=======

.. list-table:: Blur Effect samples (Samples: 8).

   * - .. figure:: /images/grease-pencil_visual-effects_blur_factor-0.png
          :width: 200px

          Original Model.

     - .. figure:: /images/grease-pencil_visual-effects_blur_factor-10.png
          :width: 200px

          Factor: 10, 10.

     - .. figure:: /images/grease-pencil_visual-effects_blur_factor-50.png
          :width: 200px

          Factor: 50, 50.

     - .. figure:: /images/grease-pencil_visual-effects_blur_factor-100.png
          :width: 200px

          Factor: 100, 100.
