.. _bpy.types.CompositorNodePixelate:

*************
Pixelate Node
*************

.. figure:: /images/compositing_node-types_CompositorNodePixelate.png
   :align: right

   Pixelate Node.

Add this node in front of a :doc:`scale node </compositing/types/distort/scale>`
to get a pixelated (non-smoothed) image from the resultant upscaled image.


Inputs
======

Color
   Standard image input.


Properties
==========

This node has no properties.


Outputs
=======

Color
   Standard image output.


Example
=======

In the compositor, check the *Use Nodes* checkbox and add an input Image node and an output Viewer node.
Connect the Input node to the viewer node and check the *Backdrop* checkbox in the header.
Open an image you would like to pixelate using the open button on the image node.
This image should now appear in the backdrop.
Now add two scale nodes between the input and output :menuselection:`Add --> Distort --> Scale`.
Change the values of X and Y to 0.2 in the first scale box and to 5 in the second.
The background image will be unchanged.

Now add a Pixelate node between the two scale nodes.

.. note::

   You can use :kbd:`Alt-V` and :kbd:`V` to zoom the backdrop in and out respectively.

.. figure:: /images/compositing_types_filter_pixelate_example.png
