.. _bpy.types.CompositorNodeAlphaOver:

***************
Alpha Over Node
***************

.. figure:: /images/compositing_node-types_CompositorNodeAlphaOver.png
   :align: right

   Alpha Over Node.

The *Alpha Over* node is used to layer images on top of one another.

Where the foreground image pixels have an alpha greater than 0, the background image will be overlaid.


Inputs
======

Factor
   Controls the amount of foreground image.
   A factor less than 1 will make the foreground more transparent.
Image
   Input for the *background* image.
Image
   Input for the *foreground* image.


Properties
==========

Convert Premultiplied
   Converts foreground image to *premultiplied alpha* format.

   The *Alpha Over* node is designed to work with *premultiplied* alpha color format.
   Use *Convert Premul* when you know that your image has *straight* alpha color values,
   to perform the correct over operation. Result will be still premultiplied alpha.

   See :term:`Alpha Channel`.

Premultiply
   The *Premul* slider allows to mix between the using *premultiplied* or *non premultiplied* alpha.

   When set to 1, the foreground color values will be multiplied by alpha, i.e. premultiplied.
   This is equivalent to enabling the *Convert Premul* option.
   When set to 0, color values does not change.

   If *Premultiply* is not zero, *Convert Premul* will be ignored.

   .. note:: This is a legacy option.


Outputs
=======

Image
   Standard image output.


Examples
========

In the map below, *Color Ramp* node is used to add an alpha channel to the black-and-white swirl image.
Then *Alpha Over* node is used to overlay it on top of another image.

.. figure:: /images/compositing_types_converter_color-ramp_create-alpha-mask.png
   :width: 600px

   Assembling a composite image using Alpha Over.

In next example, we use the *Factor* control to make a "Fade In" effect.
This effect can be animated by adding a *Time* node to feed the *Factor* socket as shown below.
In this example, over the course of 30 frames, the *Time* node makes the *Alpha Over* node produce
a picture that starts with the pure background image, and title slowly bleeds through the background.

.. figure:: /images/compositing_types_color_alpha-over_example.png
   :width: 600px

   Animated fade in effect using Alpha Over.

Note the *Convert Premul* checkbox is enabled,
since as the foreground used a PNG image that has *straight* alpha.
