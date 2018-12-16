.. _bpy.types.CompositorNodeColorMatte:

**************
Color Key Node
**************

.. figure:: /images/compositing_types_matte_color-key_node.png
   :align: right

   Color Key Node.

The color key node creates a matte based on a specified color of the input image.


Inputs
======

Image
   Standard image input.


Properties
==========

Color
   The sliders represent threshold values.
   Higher values in this node's context mean a wider range of colors from
   the specified will be added to the matte.

   Hue, Saturation, Value


Outputs
=======

Image
   Image with its alpha channel adjusted for the keyed selection.
Matte
   A black-and-white alpha mask of the key.
