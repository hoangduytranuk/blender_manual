
********************
Grease Pencil Shader
********************

.. figure:: /images/grease-pencil_materials_grease_pencil_shader_panel.png
   :align: right

   Shader panel with only Stroke component activated.

The *Grease Pencil* Shader create a material that can work
with strokes and/or filled areas of a *Grease Pencil* Object.

Stroke and fill components has it own section panel and
they can be enabled with a checkbox on the panel header.

*Stroke* only has effect on the lines and *Fill* only on the areas
determined by closed lines (by connecting the lines start and end points).

.. note::

   The shader is not yet a BSDF capable shader to interact with Blender lights
   and can only be setting up on the Material Properties panel (it is not a shader node).


Properties
==========

Stroke
------

When enabled, the shader use the stroke component.
The *Stroke* component control how to render the edit lines.

Mode Type
   Defines how to display or distribute the output material over the stroke.

   Line
      Connects every points in the strokes showing a continuous line.

   Dots
      Use a circle shape at each point in the stroke.
      The dots are not connected.

   Boxes
      Use a box shape at each point in the stroke.
      The boxes are not connected.

Style
   Type of material.

   Solid
      Use solid color.

      Color
         Color of the stroke.

   Texture
      Use image texture.

      Image
         Image data-block used as the image source.

      UV Factor
         Image size along the stroke.

      Use As Stencil Mask
         When enabled, use the image alpha as a stencil mask.

         Color
            Color to use on not transparent areas of the image.

      Mix Color
         When enabled, mix the image with a certain color.

         Factor
            Mixing amount.

         Color
            Color to mix.

.. list-table:: Samples of different material strokes mode types and styles.

   * - .. figure:: /images/grease-pencil_shader_stroke-solid-line.png
          :width: 130px

          Mode Type: Line, Style: Solid.

     - .. figure:: /images/grease-pencil_shader_stroke-texture-line.png
          :width: 130px

          Mode Type: Line, Style: Texture.

     - .. figure:: /images/grease-pencil_shader_stroke-solid-dot.png
          :width: 130px

          Mode Type: Dot, Style: Solid.

     - .. figure:: /images/grease-pencil_shader_stroke-texture-dot.png
          :width: 130px

          Mode Type: Dot, Style: Texture.


Fill
----

When enabled, the shader use the fill component.
The *Fill* component control how to render the filled areas determined by closed edit lines.

Style
   Type of material.

   Solid
      Use solid color.

      Color
         Color of the fill.

   Gradient
      Use gradient colors.

      Gradient Type

         Linear
            Mix the colors along a single axis.

         Radial
            Mix the colors radiating from a center point.

      Color.
         Primary color.

      Secondary color.
         Secondary color.

      Mix Factor
         Primary and secondary colors mixing amount.

      Flip colors
         Flips the gradient, Inverting the primary and secondary colors.

      Location
         Shift gradient position.

         X, Y

      Scale
         Scale gradient.

         X, Y

      Angle
         Rotate gradient.

   Checkerboard
      Use a checkered pattern.

      Color.
         Primary color.

      Secondary color.
         Secondary color.

      Flip colors
         Invert primary and secondary colors.

      Location
         Shift the checkered pattern position.

         X, Y

      Scale
         Overall checkered pattern scale.

      Angle
         Rotate the checkered pattern.

      Box Size
         Sets the box size of the checkered pattern.

   Texture
      Use image texture.

      Image
         Image data-block used as the image source.

      Use As Stencil Mask
         When enabled, use the image alpha as a stencil mask.

         Color
            Color to use on not transparent areas of the image.

      Offset
         Shift image position.

         X, Y

      Scale
         Scale image.

         X, Y

      Angle
         Rotate image.

      Opacity
         Image transparency.

      Clip Image
         When enabled, show one image instance only (do not repeat).

      Mix With Color
         When enabled, mix the image with a certain color.

         Factor
            Mixing amount.

         Color
            Color to mix.

.. list-table:: Samples of different material fill styles.

   * - .. figure:: /images/grease-pencil_shader_fill-solid.png
          :width: 130px

          Style: Solid.

     - .. figure:: /images/grease-pencil_shader_fill-gradient.png
          :width: 130px

          Style: Gradient.

     - .. figure:: /images/grease-pencil_shader_fill-checkerboard.png
          :width: 130px

          Style: Checkerboard.

     - .. figure:: /images/grease-pencil_shader_fill-texture.png
          :width: 130px

          Style: Texture.
