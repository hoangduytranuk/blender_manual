.. Editors Note: This page gets copied into :doc:`</render/cycles/nodes/types/converter/color_ramp>`

***************
Color Ramp Node
***************

.. figure:: /images/compositing_node-types_CompositorNodeValToRGB.png
   :align: right

   Color Ramp Node.

The Color Ramp Node is used for mapping values to colors with the use of a gradient.


Inputs
======

Factor
   The Factor input is used as an index for the color ramp.


Properties
==========

Color Ramp
   For controls see :ref:`ui-color-ramp-widget`.


Outputs
=======

Image
   Standard image output.
Alpha
   Standard alpha output.


Examples
========

Creating an Alpha Mask
----------------------

A powerful but often overlooked feature of the Color Ramp is to create an Alpha Mask,
or a mask that is overlaid on top of another image, and, like a mask,
allows some of the background to show through.
The example map below shows how to use the Color Ramp node to do this:

.. figure:: /images/compositing_types_converter_color-ramp_create-alpha-mask.png
   :width: 600px

   Using the Color Ramp node to create an alpha mask.

In the map above, a black-and-white swirl image, which is lacking an alpha channel,
is fed into the Color Ramp node as a *Factor*.
(Technically, we should have converted the image to a value using the RGB to BW node,
but hey, this works just as well since we are using a BW image as input.)

We have set the Color Ramp node to a purely transparent color on the left end of the spectrum,
and a fully Red color on the right. As seen in the viewer,
the Color Ramp node puts out a mask that is fully transparent where the image is black.
Black is zero, so Color Ramp uses the color at the left end of the spectrum,
which we have set to transparent.
The Color Ramp image is fully red and opaque where the image is white (1.00).

We verify that the output image mask is indeed transparent
by overlaying it on top of another image.


Colorizing an Image
-------------------

The real power of Color Ramp is that multiple colors can be added to the color spectrum.
This example compositing map takes a boring BW image and makes it a flaming swirl!

.. figure:: /images/compositing_types_converter_color-ramp_colorizing-image.png
   :width: 600px

In this example, we have mapped the shades of gray in the input image to three colors, blue,
yellow, and red, all fully opaque (Alpha of 1.00). Where the image is black,
Color Ramp substitutes blue, the currently selected color. Where it is some shade of gray,
Color Ramp chooses a corresponding color from the spectrum (bluish, yellow, to reddish).
Where the image is fully white, Color Ramp chooses red.
