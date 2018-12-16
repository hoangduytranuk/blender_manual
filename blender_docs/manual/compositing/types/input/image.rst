.. _bpy.types.CompositorNodeImage:

**********
Image Node
**********

.. figure:: /images/compositing_types_input_image_node.png
   :align: right

   Image Node.

The *Image* node injects any image :doc:`format that is supported by Blender </render/output/output>`.


Inputs
======

This node has no input sockets.


Properties
==========

Image
   Selection of different types of media. For controls see :ref:`ui-data-block`.
   For the options see :doc:`/editors/uv_image/image/image_settings`.

.. note::

   More options could be set in the properties region.


Outputs
=======

The first two sockets are the minimum.

Image
   Standard image output.
Alpha
   Separate Alpha value.
Z
   Z depth layer.

.. note:: Multi-Layer Format

   When a multi-layer file format, like ``EXR``, is loaded,
   each layer is made available as a socket.
