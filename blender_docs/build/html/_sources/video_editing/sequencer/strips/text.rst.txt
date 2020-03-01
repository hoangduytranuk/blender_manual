.. _bpy.types.TextSequence:

***********
Text Strips
***********

The Text strip allows you to directly display text in the Sequence editor.
The strip will display the text inserted in its text field on the final sequence.

.. tip::

   All Text strips in a video sequence can be :ref:`exported <bpy.ops.sequencer.export_subtitles>`
   as a `SubRip <https://en.wikipedia.org/wiki/SubRip>`__ file.
   This is useful when using Text strips as subtitles.


Options
=======

Text
   The actual text displayed.


Style
-----

Font
   :ref:`ui-data-block` to choose which font-file is used to render the text.
Size
   Size of the text.
Color
   The text color.
Shadow
   Creates a shadow under the text.


Layout
------

Location X/Y
   Positions the text on the X, Y axis.
Alignment X/Y
   Horizontal (X) or vertical (Y) alignment of the text relative to the location.
Wrap Width
   Wraps the text by the percentage of the frame width,
   setting this to zero disables word wrapping.


Example
=======

.. figure:: /images/video-editing_sequencer_strips_text_example.png

   Text Effect.
