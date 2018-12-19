.. _bpy.types.CompositorNodeTranslate:

**************
Translate Node
**************

.. figure:: /images/compositing_types_distort_translate_node.png
   :align: right

   Translate Node.

The translate node translates (moves) an image.

Could also be used to add a 2D Camera shake.


Inputs
======

Image
   Standard image input.
X, Y
   Used to move the input image horizontally and vertically.


Properties
==========

Relative
   Percentage translation values relative to the input image size.
Wrapping
   Repeat pixels on the other side when they extend over the image dimensions, making endless translating possible.

   None, X Axis, Y Axis, Both Axis


Outputs
=======

Image
   Standard image output.
