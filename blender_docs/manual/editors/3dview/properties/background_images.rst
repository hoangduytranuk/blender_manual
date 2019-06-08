.. _bpy.types.BackgroundImage:
.. _bpy.types.SpaceView3D.show_background_images:
.. _bpy.ops.view3d.background_image:

*****************
Background Images
*****************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> Background Image`

A background picture in your 3D View is very helpful in many situations:
modeling is obviously one, but it is also useful when painting
(e.g. you can have reference pictures of faces when painting textures directly on your model...),
or animation (when using a video as background), etc.

.. note::

   Background images are only available for orthographic views.


Settings
========

.. figure:: /images/editors_3dview_properties_background-images_panel-example.png

Axis
   Choose which views the image is visible from.
   This is helpful when you have several reference images from different views (e.g. top, front and side).
Data Source
   The source of the background image.

   Image
      Use an external image, image sequence, video file or generated texture.
   Movie Clip
      Use one of the Movie Clip data-blocks.
Opacity
   Controls the transparency of the background image.
Front/Back
   Choose whether the image is shown behind all objects, or in front of everything.
Stretch/Fit/Crop
   Controls how the image is placed in the camera view.

   Stretch
      Forces the image dimensions to match the camera bounds (may alter the aspect ratio).
   Fit
      Scales the image down to fit inside the camera view without altering the aspect ratio.
   Crop
      Scales the image up so that it fills the entire camera view,
      but without altering the aspect ratio (some of the image will be cropped).
X/Y
   Positions the background image using these offsets.

   In orthographic views, this is measured in the normal scene units.
   In the camera view, this is measured relative to the camera bounds
   (0.1 will offset it by 10% of the view width/height).
Flip Horizontally
   Swaps the image around, such that the left side is now on the right, and the right now on the left.
Flip Vertically
   Swaps the image around, such that the top side is now on the bottom, and the bottom now on the top.
Rotation
   Rotates the image around its center.
Size
   Scales the image up or down from its center.
