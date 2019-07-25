
************
Introduction
************

Sequencer preview is used to display result of rendering Sequencer timeline.
This can be further configured to display output from certain channel, overlay or image analyzer (scope).


Header
======

.. figure:: /images/sequencer_preview_introduction_header.png

   Sequencer Display header.


View Menu
---------

Fit preview in window :kbd:`Home`
   Resize the preview so that it fits in the window.
Zoom :kbd:`Shift-B`
   Click and drag to draw a rectangle and zoom to this rectangle.
Fractional zoom
   Resize the preview in steps from 1:8 to 8:1.
Safe Areas
   Display an overlay on the preview, marking where title safe region is.
Show Metadata
   Display Image metadata in the preview area.
Sequence Render Image
   Render image at playhead position.
Sequence Render Animation
   Render timeline from Preview Start to Preview End Frame to a Video file or series of images.


Display Mode
------------

Mode to show different aspects of the composite result,
for the current frame:

Image Preview
   Render image preview.
Luma Waveform
   Brightness/contrast analyzer.
Chroma Vectorscope
   Color hue and saturation analyzer.
Histogram
   RGB distribution histogram.


Display Channels
----------------

Color and Alpha
   Display preview image with transparency over checkerboard pattern.
Color
   Ignore transparency of preview image (fully transparent areas will be black).

..
   You can adjust the view by zooming in with :kbd:`Plus` and zoom out with :kbd:`Minus`.


Gizmos
======

You can use gizmos to pan and zoom image in the Sequencer preview region.
