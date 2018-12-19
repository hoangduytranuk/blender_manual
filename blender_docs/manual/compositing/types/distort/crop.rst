.. _bpy.types.CompositorNodeCrop:

*********
Crop Node
*********

.. figure:: /images/compositing_types_distort_crop_node.png
   :align: right

   Crop Node.

The Crop Node takes an input image and crops it to a selected region.


Inputs
======

Image
   Standard image input.


Properties
==========

Crop Image Size
   When enabled, the image size is cropped to the specified region.
   When disabled, the image remains the same size, and uncropped areas become transparent pixels.
Relative
   When enabled, crop dimensions are a percentage of the image's width and height.
   When disabled, the range of the *Crop Region Values* are the width and height of the image in pixels.
Crop Region Values
   Define borders of the crop region.

   lower, upper, left, right


Outputs
=======

Image
   Standard image output.
