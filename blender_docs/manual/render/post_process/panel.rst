
*********************
Post Processing Panel
*********************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Render --> Post Processing`

The Post Processing panel is used to control different options used to process your image after rendering.

.. figure:: /images/render_post-process_panel_panel.png
   :align: right

   Post Processing panel.

Sequencer
   Renders the output of the Video Sequence editor, instead of the view from the 3D scene's active camera.
   If the sequence contains scene strips, these will also be rendered as part of the pipeline.
   If *Compositing* is also enabled, the Scene strip will be the output of the Compositor.
Compositing
   Renders the output from the compositing node setup,
   and then pumps all images through the Composite node map,
   displaying the image fed to the Composite Output node.


Dithering
=========

Dithering is a technique for blurring pixels to prevent banding that is seen in areas of
gradients, where stair-stepping appears between colors.
Banding artifacts are more noticeable when gradients are longer, or less steep.
Dithering was developed for graphics with low bit depths,
meaning they had a limited range of possible colors.

Dithering works by taking pixel values and comparing them with a threshold and
neighboring pixels then does calculations to generate the appropriate color.
Dithering creates the perceived effect of a larger color palette by creating a sort of visual color mixing.
For example, if you take a grid and distribute red and yellow pixels evenly across it,
the image would appear to be orange.

The *Dither* value ranges from 0 to 2.

.. note::

   When using *Blender Internal* Render you get a few more options and these are discussed
   :doc:`here </render/blender_render/post_processing/index>`.
