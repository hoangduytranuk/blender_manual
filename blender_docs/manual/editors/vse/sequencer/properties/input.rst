.. _bpy.types.SequenceCrop:

*****************
Strip Input Panel
*****************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> Strip --> Strip Input`

.. figure:: /images/editors_vse_sequencer_properties_input_panel.png
   :align: right

   Strip Input settings.

The Strip Input panel is used to controls the source,
the duration of the strip along with some basic transforms.

Path
   A text field that lets you edit/update the path of the file used by a strip.
   When you moved the files, it avoids having to delete and re-create the strip.
File
   Same than before, but in case you renamed the source file, you can retrieve it (or change it).
Color Space
   To specify the color space of the source file.
Alpha mode
   If the source file has an Alpha (transparency) channel, you can choose:

   :term:`Straight Alpha` or :term:`Premultiplied Alpha`
Change Data/File
   Same as the *Path* and *File* fields, but
   this time combined to open the File Browser in order to find the file(s) you search.
   :menuselection:`Strip --> Change --> Paths/files`

MPEG Preseek
   Movie strip only -- Use the Preseek field to tell Blender to look backward and
   compose the image based on the n previous frames (e.g. 15 for Mpeg2 DVD).
Stream index
   Movie strip only -- For files with several movie streams, use the stream with the given index.

Image Offset
   Used to translate the frames along the X and Y axis.
   Additionally it disables the auto-scaling of the image.
Image Crop
   Used to crop the source image, use *Top*, *Left*,
   *Bottom*, and *Right* to control which part of the image is cropped.

.. _sequencer-duration-hard:

Trim Duration (hard)
   Controls at what frame the source of the strip starts and ends at.
Trim Duration (soft)
   Can be used to either extend the strip beyond the end frame by repeating the last frame.
   Or it can be used to shorten the strip, as if you were cropping the end frame.
   This is the same has adjusting the strip handles.
