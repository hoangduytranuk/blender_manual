
********
Viewport
********

Display
=======

Object Info
   Display the active Object name and frame number at the bottom left of the 3D View.
View Name
   Display the name and type of the current view in the top left corner of the 3D View.
   For example: "User Perspective" or "Top Orthographic".
Playback FPS
   Show the frames per second screen refresh rate while an animation is played back.
   It appears in the viewport corner, displaying red if the frame rate set cannot be reached
Gizmo size
   Diameter of the manipulator.
Look Dev Sphere Size
   Diameter of the LookDev sphere overlay.
3D Viewport Axis
   TODO 2.8.


.. _prefs-system-multi-sampling:

Quality
=======

Viewport Anti-aliasing
   TODO 2.8.
Multisampling
   This enables :term:`FSAA` for smoother drawing, at the expense of some performance.
Grease Pencil Multisampling
   TODO.
Edit-Mode Smooth Wires
   TODO 2.8.


Textures
========

Limit Size
   Limit the maximum resolution for pictures used in textured display to save memory.
   The limit options are specified in a square of pixels
   (e.g: the option 256 means a texture of 256×256 pixels). This is useful for game engineers,
   whereas the texture limit matches paging blocks of the textures in the target graphic card memory.
Anisotropic Filtering
   Sets the level of anisotropic filtering.
   This improves the quality of how textures are drawn at the cost of performance.
Clip Alpha
   Clip alpha below this threshold in the 3D View.
   Note that, the default is set to a low value to prevent issues on some GPU's.
Image Display Method
   Method to draw images as the following options are supported:

   Automatic
      Automatically use *GLSL* which runs on the GPU for performance but falls back to
      the CPU for large images which might be slow when loaded with the GPU.
   2D Texture
      Uses CPU for display transform and draws images as a 2D texture.
   GLSL
      Fastest method using GLSL for display transform and draws images as a 2D texture.


Selection
=========

OpenGL Depth Picking
   This option uses an alternative method of picking which uses depth information to select the front-most elements.
   It is only used for selecting with the cursor (not border select, lasso, circle select, etc.).

   Performance varies depending on your OpenGL hardware and drivers.
