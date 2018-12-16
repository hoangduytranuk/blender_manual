
***********
Motion Blur
***********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Motion Blur`

Blender's animations are by default rendered as a sequence of *perfectly still* images.
While great for stop-motion and time-lapses, this is unrealistic, since fast-moving
objects do appear to be blurred in the direction of motion,
both in a movie frame and in a photograph from a real-world camera.

.. figure:: /images/render_cycles_settings_scene_render_motion-blur_example.jpg
   :width: 640px

   Motion blur example (camera zoom).

.. note::

   If there are particles or other physics system in a scene,
   be sure to bake them before rendering,
   otherwise you might not get correct or consistent motion.


Options
=======

.. figure:: /images/render_cycles_settings_scene_render_motion-blur_settings.png
   :align: right

   Motion Blur settings.

Position
   Controls at what point the shutter opens in relation to the current frame.

   Start on Frame
      Shutter is starting to open at the current frame.
   Center on Frame
      Shutter is fully opened at the current frame.
   End on Frame
      Shutter is fully closed at the current frame.

Shutter (Speed)
   Time (in frames) between when the shutter starts to open and fully closed.
   For example, shutter time 1.0 blurs over the length of 1 frame.
Shutter Curve
   Curve defining how the shutter opens and closes.

   The X axis is time, Y values of 0 means fully closed shutter, Y values of 1 means fully opened shutter.
   Default mapping is set to when shutter opens and closes instantly.

Shutter Type
   Creates a "rolling shutter" effect.

   In real CMOS cameras the sensor is read out with scanlines
   and hence different scanlines are sampled at a different moment in time.
   This, for example, make vertical straight lines being curved when doing a horizontal camera pan.

   None
      No rolling shutter effect.
   Top-Bottom
      Renders rolling shutter from the top of the image to the bottom.

Rolling Shutter Duration
   Controls balance between pure rolling shutter effect (if the value is zero)
   and pure motion blur effect (if the value is one).

.. warning::

   An object modifier setup that changes mesh topology over time can not render
   deformation motion blur correctly. Deformation blur should be disabled for such objects.

   Common examples of this are animated Booleans, Deformation before Edge Split, Remesh, Skin or Decimate modifiers.

.. seealso::

   Each object has its own settings to control motion blur.
   These options can be found in the Object tab of the Properties editor.
   See :ref:`object setting <render-cycles-settings-object-motion-blur>` for more information.


Example
=======

.. figure:: /images/render_cycles_settings_scene_render_motion-blur_example-cubes.jpg
   :width: 640px

   Motion blur example.
   (`blend-file <https://en.blender.org/uploads/0/03/Blender2.65_motion_blur.blend>`__)
