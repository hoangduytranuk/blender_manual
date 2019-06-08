.. (Todo move) to data_system: shared with Movie editor?

**************
Image Settings
**************

Image Menu
==========

New Image
   Creates a new :ref:`image-generated` Image.
Open Image
   Load image from a file.
Read Render Layers
   Read all the current scene's render layers from cache, as needed.
   This can be used to save RAM while rendering because the render layers do not have to be saved in RAM.
   This can also be used to recover some information from a fail render.
   For this to work, :ref:`Save Buffers <render_properties_save-buffers>` must be enabled.
Save All Images
   Repack (or save if external file) all edited images.
Replace Image
   Replaces the current image, while preserving the link to UV maps,
   with a selected file.
Reload Image
   Reloading the image from an external file.
Save Image
   Save the image, if the image is already a file :kbd:`Alt-S`.
Save As Image
   Save the (rendered) image in a separate file :kbd:`F3` or
   you want to save it under a different name.
Save a Copy
   Using *Save as Copy* will save the file to a specified name,
   but will keep the old one open in the Image editor.
Edit Externally
   Using the *Edit Externally* tool Blender will open an external image editor,
   as specified in the *Preferences* and load in the image to be edited.
Invert
   Invert Image Colors
      Invert the colors of an image.
   Invert Channel
      Red, Green, Blue, Alpha
Pack
   Pack Image
      Packs the external image file into the blend-file.
      See :ref:`pack-unpack-data`.
   Pack As PNG
      Packs the image into the blend-file as lossless PNG.
      It is available as an option in the Operator panel
      or if the image was modified inside Blender and changes are not saved to the drive.

.. important::

   Rendered images had to be saved externally or packed.

Image Panel
===========

.. figure:: /images/editors_uv-image_image_image-settings_movie-image-panel.png
   :align: right

   Image panel.

Image
   Data-block menu.

   New ``+``
      The *New Image* button opens a pop-up to configure a `Generated`_ image.


Source
------

See about supported :doc:`/files/files/media/image_formats`.


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

.. list-table::

   * - .. figure:: /images/editors_uv-image_image_image-settings_generated-image-panel.png

          Image panel for Generated source.

     - .. figure:: /images/editors_uv-image_image_image-settings_generated-new-image.png

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
      Opens the :doc:`/editors/file_browser/index` to select a file from a drive.
   Reload
      Reloads the file. Useful when a file has been reworked in an external application.
Color Space
   :term:`Color Space`.

   XYZ
      XYZ space.
   sRGB
      Standard RGB display space.
   Raw
      Raw space.
   Non-Color
      Color space used for images which contains non-color data (e.g. normal maps).
   Linear ACES
      ACES linear space.
   Linear
      Linear 709 (full range). Blender native linear space.
   Filmic Log
      Todo.
View as Render
   Applies :doc:`color transform </render/color_management>` when displaying this image on the screen.
Use Multi-View
   See :doc:`Multi-View </render/output/multiview/index>`.
Alpha
   :term:`Alpha Channel`.

   Straight, Premultiplied
