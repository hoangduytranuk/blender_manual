
********************
UV Along Stroke Node
********************

.. figure:: /images/render_freestyle_parameter-editor_line-style_nodes_uv-along-stroke_node.png
   :align: right

   UV Along Stroke Node.

The *UV Along Stroke* input node is maps textures along the stroke length,
making it possible to mimic pencil, paintbrush, and other art medium marks.

In Blender Render equivalent options can be found in
:menuselection:`Properties editor --> Texture --> Mapping` panel.

.. note::

   These UV maps become available only during the Freestyle rendering process.
   Hence, the UV Along Stroke node cannot be replaced by the conventional UV Map input node
   which takes an existing UV map already defined as part of mesh data.


Inputs
======

This node has no inputs.


Properties
==========

Use Tips
   Allows to use lower quarters of a texture image for the head and tail tips of a stroke,
   while the upper half for the stroke body.


Outputs
=======

UV
   UV maps defined along strokes.


Example
=======

The following screen capture shows a typical shader node tree that maps a floral texture image along strokes.
The UV Along Stroke input node retrieves UV maps defined by Freestyle along generated strokes, and
feeds them to the Vector input channel of the Image Texture node.
A texture image is selected in the Image Texture node,
and its color is fed to the Alpha channel of the Line Style Output node.
Since the Alpha Factor is set to one, the texture image replaces the base alpha transparency of the active line style
(shown in the Freestyle Line Style panel).
On the other hand, the Mix blend mode is selected in the Line Style Output node with the Color Factor set to zero,
so that the gradient line color specified in the active line style is applied along strokes.

.. figure:: /images/render_freestyle_parameter-editor_line-style_nodes_uv-along-stroke_example.png

   `.blend <https://wiki.blender.org/wiki/File:Blender_272_textured_strokes_in_cycles.blend>`__.

It is noted that the texture image ``FS_floral_brush.png``
shown in the screen capture is an example of Freestyle brush images with tips.
Specifically, the upper half of the image is used as a seamless horizontal tile of the stroke body,
whereas the parts in the lower half are tips (stroke caps) at both ends of the stroke.
