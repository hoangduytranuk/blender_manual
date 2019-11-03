.. _bpy.types.CompositorNodeLevels:

***********
Levels Node
***********

.. figure:: /images/compositing_node-types_CompositorNodeLevels.png
   :align: right

   Levels Node.

The Levels Node read the inputs color channels
and outputs analytical values.


Inputs
======

Image
   Standard image input.


Properties
==========

Channel
   C (Combined RGB), R (Red), G (Green), B (Blue), L (Luminance)


Outputs
=======

1D values based on the levels of an image.

Mean
   The mean is the average value of all image pixels in specified channel
   (combined, red, green, blue, luminance). It tells you how dark or bright the image
   is and can be used as such for setups that depend on how is input "bright" or "dark".
Standard deviation
   How much those pixel values differ from the mean.
   A low standard deviation indicates that the pixel values tend to be very close to the mean.
   A high standard deviation indicates that the values are spread out over a large range of values.

The visualization of such data is just a gray rectangle.
