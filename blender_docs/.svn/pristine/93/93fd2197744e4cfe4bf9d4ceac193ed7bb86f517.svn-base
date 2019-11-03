.. (Todo move) to data_system: shared with Movie editor?

**************
Image Settings
**************

Image Menu
==========

New
   Creates a new :ref:`image-generated` Image.
Open
   Load image from a file.
Open Cache Render
   Load the current scene's render layers from disk cache, if available.
   This can be used to save RAM while rendering because the render layers do not have to be saved in RAM.
   This can also be used to recover some information from a fail render.
   For this to work, :ref:`Save Buffers <render_properties_save-buffers>` must be enabled.

Replace
   Replaces the current image throughout the blend-file with another image.
Reload
   Reload the image from the file on disk.
Edit Externally
   Using the *Edit Externally* tool Blender will open an external image editor,
   as specified in the *Preferences* and load in the image to be edited.

Save
   Save the image, if the image is already a file :kbd:`Alt-S`.
Save As
   Save the (rendered) image in a separate file :kbd:`Shift-S` or
   you want to save it under a different name.
Save a Copy
   Using *Save as Copy* will save the file to a specified name,
   but will keep the old one open in the Image editor.
Save All Images
   Save all modified images. Packed images will be repacked.

Invert
   Invert Image Colors
      Invert the colors of an image.
   Invert Channel
      Red, Green, Blue, Alpha

Pack
   Packs the image into the blend-file.
   See :ref:`pack-unpack-data`.
Unpack
   Unpack the image to disk.

.. important::

   Rendered images are not automatically saved, they have to be saved to disk manually.


Image Panel
===========

.. TODO2.8
   .. figure:: /images/editors_uv-image_image_image-settings_movie-image-panel.png
      :align: right

      Image panel.

Image
   Data-block menu.

   New ``+``
      The *New Image* button opens a pop-up to configure a `Generated`_ image.


Source
------

See about supported :doc:`/files/media/image_formats`.


Single Image
^^^^^^^^^^^^

Still image or a single frame.


Image Sequence
^^^^^^^^^^^^^^

Each frame is stored in a separate file.
How to :ref:`image-formats-open-sequence`.

Frame
   A label showing the current frame.
Further options
   See `Movie`_ below.


Movie
^^^^^

Frames packed into a container.

Deinterlace
   Removes fields in a video file. For example,
   if it is an analog video and it has even or odd interlacing fields.
Frame
   Frames
      Sets the range of frames to use.
   Start
      Global starting frame of the sequence, when the playback should start.
      This is a global setting which means it affects all clip users such as the Movie Clip editor itself,
      motion tracking constraints and compositor nodes.
   Offset
      Offsets the first frame of the clip. It adds an extra offset to the frame number when
      converting a scene frame to the frame number in the file name.
      This option does not affect tracking data or any other associated data.
Match Movie Length
   This button sets image's user's length to the one of selected movie.
Auto Refresh
   Automatically refresh images on frame changes.
Cyclic
   Start over and repeats after the last frame to create a continuous loop.


.. _image-generated:

Generated
^^^^^^^^^

Image generated in Blender.

.. TODO2.8
   .. list-table::

      * - .. figure:: /images/editors_image_image-settings_generated-image-panel.png

             Image panel for Generated source.

        - .. figure:: /images/editors_image_image-settings_generated-new-image.png

             The New Image pop-up menu.

Width, Height
   The size of image in pixels.
Color
   Sets the fill color if creating a blank image.
32 bit Float / Float Buffer
   Creates a 32 bit image. This is a larger file size,
   but holds much more color information than the standard 8 bit image.
   For close ups and large gradients, it may be better to use a 32 bit image.
Type
   Blank
      Creates a Blank image of a single specified color.
   UV Grid
      Creates a checkerboard pattern with a colored cross (+) in each square.
   Color Grid
      Creates a more complex colored grid with letters and numbers denoting locations in the grid.
      It could be used for testing how the UVs have been mapped and to reduce stretching or distortion.


Common Options
--------------

File
   Use for replacing or packing files.

   Pack
      Embed the resource into the current blend-file.
   Path
      Path to the linked file.
   Open
      Opens the :doc:`/editors/file_browser` to select a file from a drive.
   Reload
      Reloads the file. Useful when a file has been reworked in an external application.
Color Space
   :term:`Color Space`.

   sRGB
      Standard RGB display space.
   Linear
      Linear 709 (full range). Blender native linear space.
   Linear ACES
      ACES linear space.
   XYZ
      Standard linear XYZ space.
   Non-Color
      Color space used for images which contains non-color data (e.g. normal maps).
   Raw
      Same as Non-Color.
   Filmic Log
      Intermediate log color space of Filmic view transform.
View as Render
   Applies :doc:`color transform </render/color_management>` when displaying this image on the screen.
Use Multi-View
   See :doc:`Multi-View </render/output/multiview/index>`.
Alpha
   Representation of alpha in the image file, to convert to and from when saving and loading the image.
   See :term:`Alpha Channel`.

   Straight
      Store RGB and alpha channels separately with alpha acting as a mask, also known as unassociated alpha.
      Commonly used by image editing applications and file formats like PNG.
      This preserves colors in parts of the image with zero alpha.
   Premultiplied
      Store RGB channels with alpha multiplied in, also known as associated alpha.
      The natural format for renders and used by file formats like OpenEXR.
      This can represent purely emissive effects like fire correctly, unlike straight alpha.
   Channel Packed
      Different images are packed in the RGB and alpha channels, and they should not affect each other.
      Channel packing is commonly used by game engines to save memory.
   None
      Ignore alpha channel from the file and make image fully opaque.
