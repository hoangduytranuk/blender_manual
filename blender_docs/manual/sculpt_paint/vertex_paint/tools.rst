
*****
Tools
*****

The *Tool Shelf* contains most of the options for vertex painting.
The following sections describe the controls in each of the available panels.

.. figure:: /images/sculpt-paint_painting_vertex-paint_tools_tab.png
   :align: right

   Vertex Painting options.


Brush
=====

Brush
   The :doc:`brush presets </sculpt_paint/brush/settings>` data-block menu.
Color
   The color of the brush. See :ref:`ui-color-picker`.

   Press :kbd:`S` on any part of the image to sample that color and set it as the brush color.
   Hold :kbd:`Ctrl` to paint with background color.

   Flip (cycle icon) :kbd:`X`
      Swaps the foreground and background color.

   .. note::

      Note that Vertex Paint works in sRGB :term:`space <Color Space>`,
      and the RGB representation of the same colors will be different
      between the paint tools and the materials that are in linear space.

Radius
   Set the radius of the brush.
Strength
   Set the strength of the brush's effect.
Blend
   See :term:`Color Blend Modes`.

   In addition, here you can select the *Blur* or *Smear* mode.
Alpha
   When this is disabled, it locks (prevents changes) the alpha channel while painting.
Accumulate
   This will allow a stroke to accumulate on itself, just like an airbrush would do.
Front Faces Only
   Only paint on the front side of faces.
Falloff Angle
   As faces point away from the view the brush strokes fade away to prevent harsh edges.

   Angle
      The angle at which the falloff begins.
2D Falloff
   This turns the brush influence into a cylinder (the depth along the view is ignored) instead of a sphere.


Texture
=======

See :doc:`/sculpt_paint/brush/texture`.


Stroke & Curve
==============

See :doc:`/sculpt_paint/brush/stroke_curve`.


Symmetry
========

(Todo)


Color Tools
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Vertex Paint Mode
   :Menu:      :menuselection:`Paint`

.. (TODO) tooltips, each tool has parameters

Bright/Contrast
   Adjust vertex color brightness/contrast.
Hue Saturation Value
   Adjust vertex color HSV values.
Levels
   Adjust levels of vertex colors.
Invert
   Invert RGB values.
Vertex Color from Weight
   Converts the active weight into grayscale vertex colors.
Dirty Vertex Colors
   Blur Strength
      Blur strength per iteration.
   Blur Iterations
      Number of times to blur the colors (higher blurs more).
   Highlight Angle
      Less than 90 limits the angle used in the tonal range.
   Dirt Angle
      Less than 90 limits the angle used in the tonal range.
   Dirt Only
      When active it won't calculate cleans for convex areas.
Smooth Vertex Colors
   Smooth colors across vertices.
Set Vertex Colors :kbd:`Shift-K`
   Fill the active vertex color layer with the current paint color.

.. seealso::

   :doc:`/sculpt_paint/weight_paint/hide_mask`
