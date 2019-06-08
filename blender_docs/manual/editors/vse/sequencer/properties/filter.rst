.. _bpy.types.EffectSequence:

************
Filter Panel
************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> Strip --> Filter`

.. figure:: /images/editors_vse_sequencer_properties_filter_panel.png
   :align: right

Enables you to quickly set common image pre-processing options.


Video
=====

Strobe
   To only display each nth frame. For example, if you set this to 10,
   the strip will only display frames 1, 11, 21, 31, 41... of the source.
   *Strobe* is a float value -- this way you can get a strobe effect synced exactly to a beat,
   for example, by using non-integer values.

Reverse
   Plays the strip in reverse (time).
Deinterlace
   Removes fields in a video file. For example,
   if it is an analog video and it has even or odd interlacing fields.

X Flip
   Mirrors the image along the X axis (left to right).
Y Flip
   Mirrors the image along the Y axis (top to bottom).


Color
=====

Saturation
   Increase or decrease the saturation of an image.
Multiply
   Multiplies the colors by this value. This will increases the brightness.

Convert to Float
   Converts input to float data.
