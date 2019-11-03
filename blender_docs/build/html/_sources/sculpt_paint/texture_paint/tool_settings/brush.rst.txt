
*****
Brush
*****

.. figure:: /images/sculpt-paint_texture-paint_tools_brush-settings.png
   :align: right

   Brush settings.


Radius
   The radius of the brush in pixels.

Strength
   How powerful the brush is when applied.

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

      In order to see the effects of the Erase and Add Alpha mix modes in the Image Editor,
      you must enable the alpha channel display by clicking the Display Alpha or the Alpha-Only button.
      Transparent (no alpha) areas will then show a checkered background.


Color Picker
============

Color
-----

The color of the brush. See :ref:`ui-color-picker`.

Press :kbd:`S` on any part of the image to sample that color and set it as the brush color.
Hold :kbd:`Ctrl` while painting to temporally paint with the secondary color.

Flip (cycle icon) :kbd:`X`
   Swaps the primary and secondary colors.


Gradient
--------

A gradient can be used as a color source.

Gradient Colors
   The :ref:`ui-color-ramp-widget` to define the gradient colors.
Mode
   Pressure
      Will choose a color from the color ramp according to the stylus pressure.
   Clamp
      Will alter the color along the stroke and as specified by *Gradient Spacing* option.
      With *Clamp* it uses the last color of the color ramp after the specified gradient.
   Repeat
      Similar to *Clamp*. After the last color it resets the color to the first color in the color ramp and
      repeats the pattern.


Color Palette
=============

Color Palettes are a way of storing a brush's color so that it can be used at a later time.
This is useful when working with several colors at once.

Palette
   A :ref:`ui-data-block` to select a palette.

New ``+``
   Adds the current brush's primary *Color* to the palette.
Delete ``-``
   Removes the currently selected color from the palette.

Color List
   Each color that belongs to the palette is presented in a list.
   Clicking on a color will change the brush's primary *Color* to that color.


Options
=======

Accumulate
   This will allow a stroke to accumulate on itself, just like an airbrush would do.
Adjust Strength for Spacing
   Attenuate the brush strength according to spacing.
Affect Alpha
   When this is disabled, it locks (prevents changes to) the alpha channel while painting (3D only).


.. move? this is not part of the brush panel

Tiling
======

.. admonition:: Reference
   :class: refbox

   :Editor:    Image Editor
   :Mode:      Paint Mode
   :Menu:      :menuselection:`Sidebar --> Tools --> Tiling`

Wraps the stroke to the other side of the image as your brush moves off the opposite side of the canvas.
Very handy for making seamless textures.

   X
      left/right
   Y
      top/bottom
