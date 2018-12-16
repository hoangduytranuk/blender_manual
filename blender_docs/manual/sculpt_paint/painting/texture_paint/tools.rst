
*****
Tools
*****

Tools located in the *Tools* tab of the *Tool Shelf* in the 3D View or UV/Image Editor.


Brush
=====

.. figure:: /images/sculpt-paint_painting_texture-paint_tools_brush-settings.png
   :align: right

   Brush settings.

With this panel, you can create many brushes, each with unique settings (such as color and width).
In the UV/Image Editor this panel is called *Paint*.


Brush Types
-----------

Texture Draw
^^^^^^^^^^^^

The normal brush, paints a swath of color.
See `Common`_ settings below.

Use Gradient
   A gradient can be used as a color source.

   Gradient Colors
      The :ref:`ui-color-ramp-widget` to define the gradient colors.
   Mode
      Pressure
         Will choose a color from the color ramp according to the stylus pressure.
      Clamp
         Will alter the color along the stroke and as specified by *Gradient spacing*.
         With Clamp it uses the last color of the color ramp after the specified gradient.
      Repeat
         Similar to *Clamp*. After the last color it resets the color to the first color in the color ramp and
         repeats the pattern.


Fill
^^^^

It can be used to fill large areas of the image with the brush color.
The tool fills adjacent pixels that have a color value similar to the pixel you clicked on.

Fill Threshold (2D only)
   Determines how much the color must be similar to the color of pixel you click to be filled.
   A low *Threshold* only fills very similar in color pixels.
   A higher *Threshold* fills pixels within a broader range of color.

Use Gradient
   Allows the use of a gradient to fill the image.

   To apply the gradient with the *Fill* brush click :kbd:`LMB` and drag to define
   the gradient line, or radius if a radial gradient is used (depending on the *Gradient Fill Mode*).

   Gradient Colors
      The :ref:`ui-color-ramp-widget` to define the gradient colors.

   Gradient Fill Mode
      Linear, Radial

.. note:: Overrides

   For projective texturing it will bypass some options for projective painting to paint the model.
   This means that occluded, backfacing and normal culled faces will always get filled,
   regardless of whether the options are activated
   in the :doc:`Project Paint </sculpt_paint/painting/texture_paint/options>` panel.


Mask
^^^^

The mask feature maps an image to the mesh and uses the image intensity to
mask out certain parts of the mesh out during painting.
The mask options can be found in the mask panel's
:doc:`slots tab </sculpt_paint/painting/texture_paint/slots_mask>`.
It's only available for 3D projective painting.

Mask Value
   Mask weight, a value of zero means not masked, while one is completely masked.


Soften
^^^^^^

Uses a "blur effect" to soften or sharpen the image.

Direction
   Soften
      Is used to paint a blur effect.

      Kernel Radius (2D only)
         Blur radius in pixels.
   Sharpen
      The Sharpen tool enhances the contrast of the image as you paint over it.

      Sharp Threshold
         The Threshold will only apply sharpening to only those pixels that
         differ more than the threshold value from their surrounding pixels.
      Kernel Radius (2D only)
         The kernel size controls how big an area the tool searches over is while calculating that difference.
Blur Mode
   The blur kernel type controls how neighboring pixels are weighted when calculating the blur effect.

   Gaussian
      Gaussian will sample the pixels near the center of the brush most.
   Box
      Box samples all surrounding pixels equally.


Smear
^^^^^

When you click, takes the colors under the cursor, and blends them in the direction you move the mouse.
Similar to the "smudge" tool of *Gimp*.


Clone
^^^^^

Copies the colors from the specified image (or location of the same image) to the active image.

In 3D projective painting the clone cursor can be set with :kbd:`Ctrl-LMB`.
In 2D painting the clone can be moved dragging it with :kbd:`RMB`.

Clone from Paint Slot (3D projective only)
   Use another image as clone source, instead of using the 3D cursor position as the source in the same image.

   Source Clone Slot
      This allows you to select an image as a clone source.

Image (2D only)
   Image used as a clone source.
Alpha (2D only)
   Opacity of the clone image display.


Common
------

Most brushes have common settings.

Color
   The color of the brush. See :ref:`ui-color-picker`.

   Press :kbd:`S` on any part of the image to sample that color and set it as the brush color.
   Hold :kbd:`Ctrl` to paint with background color.

   Flip (cycle icon) :kbd:`X`
      Swaps the foreground and background color.
Radius
   The radius of the brush in pixels.
Strength
   How powerful the brush is when applied.

   Space Attenuation (padlock icon)
      Attenuate the brush strength according to spacing.
Pressure Sensitivity (hand and bulged in blue line icon)
   The toggle to the right of the following three settings will
   enable or disable tablet pressure sensitivity to control how strong the effect is.

Blend
   Set the way the paint is applied over the underlying color. See :term:`Color Blend Modes`.

   - Add Alpha: makes the image more opaque where painted.
   - Erase Alpha: makes the image transparent where painted,
     allowing background colors and lower-level textures to show through.
     As you "paint", the false checkerboard background will be revealed.
     Using a table pen's eraser end will toggle on this mode.

   .. tip::

      In order to see the effects of the Erase and Add Alpha mix modes in the UV/Image Editor,
      you must enable the alpha channel display by clicking the Display Alpha or the Alpha-Only button.
      Transparent (no alpha) areas will then show a checkered background.

Accumulate
   This will allow a stroke to accumulate on itself, just like an airbrush would do.
Alpha (3D only)
   When this is disabled, it locks (prevents changes to) the alpha channel while painting.

.. tip:: Masking

   Use the face selection mask to isolate faces.
   See :doc:`Face Selection Masking </sculpt_paint/painting/weight_paint/hide_mask>` details.


Tilling
=======

Wraps the stroke to the other side of the image as your brush moves off the opposite side of the canvas.
Very handy for making seamless textures. (In the *UV/Image Editor* only.)

   X
      left/right
   Y
      top/bottom


External
========

(Todo)

Quick Edit
   Edit a snapshot of the viewport in an external image editor.
Apply
   Project edited image back onto the object.
Size
   Size of the captured image for reprojecting.
Apply Camera Image
   Project an edited render from the active camera back onto the object.
