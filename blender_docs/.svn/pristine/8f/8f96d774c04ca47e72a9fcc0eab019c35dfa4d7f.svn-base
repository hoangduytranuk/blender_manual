
************
Introduction
************

The Image Editor is where you can view/edit 2D assets like images or textures.

.. figure:: /images/editors_image_introduction_main.png

   Image Editor with a test grid texture.


Toolbar
=======

Sample Tool
   Used to sample a pixel's color from anywhere within Blender.

   Sample Size
      The dimensions of the square used to sample underlying pixels.
      If larger than 1 the resulting sample is an average of all underlying pixels.

Annotate
   See :doc:`Annotations </interface/annotate_tool>` for more information.


Header
======

Menus
-----

View
   Tools for controlling how the content is displayed in the editor.
   See :doc:`/editors/image/navigating`.
Image
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
      Reload the image from the file on drive.
   Edit Externally
      Using the *Edit Externally* tool Blender will open an external image editor,
      as specified in the *Preferences* and load in the image to be edited.

   Save
      Save the image, if the image is already a file :kbd:`Alt-S`.
   Save As
      Save the (rendered) image in a separate file :kbd:`Shift-Alt-S` or
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

   Resize
      Adjust the image size in pixels.
   Pack
      Packs the image into the blend-file.
      See :ref:`pack-unpack-data`.
   Unpack
      Unpack the image to a drive.
   Extract Palette
      Extracts a :ref:`Color Palette <ui-color-palette>` from the image for use by other tools.
   Generate Grease Pencil
      Creates a :doc:`Grease Pencil </grease_pencil/index>` object using the currently selected image as a source.


   .. important::

      Rendered images are not automatically saved, they have to be saved to drive manually.


Controls
--------

Image
   A :ref:`data-block menu <ui-data-block>` used for selecting images.
   When an image has been loaded or created in the Image editor,
   the Image panel appears in the *Sidebar region*.
   See :doc:`/editors/image/image_settings`.

      - Render Result
      - Viewer Node
Modes
   View
      Displays Images.
   Paint
      :doc:`/sculpt_paint/texture_paint/index`.
   Mask
      :doc:`/movie_clip/masking/index`.


Multi-Layer
^^^^^^^^^^^

When a rendered image is displayed in the Image Editor,
several new menu items become available.

Slot
   You can save successive renders into the render buffer by selecting a new slot
   before rendering. If an image has been rendered to a slot, it can be viewed by
   selecting that slot. Empty slots appear as blank grids in the Image editor.
   Use the :kbd:`J` and :kbd:`Alt-J` to cycle forwards and backwards through saved renders.
   Alternatively you can use the number keys :kbd:`1`, :kbd:`2`, :kbd:`3`, etc,
   to select the slot with the corresponding number. A slot can be renamed by
   double clicking its name in the Image panel in the Sidebar.
View Layer
   If you are using :doc:`View Layers </render/layers/index>`,
   use this menu to select which layer is displayed.
Render Pass
   If you are using :doc:`Render Passes </render/layers/passes>`,
   use this menu to select which pass is displayed.


Display Channels
^^^^^^^^^^^^^^^^

In the dropdown menu on the right, the displayed channels can be selected.

Color and Alpha
   Replaces transparent pixels with background checkerboard, denoting the alpha channel.
Color
   Display the colored image, without alpha channel.
Alpha
   Displays the Alpha channel a grayscale image. White areas are opaque, black areas have an alpha of 0.
Z-Buffer
   Display the depth from the camera, from Clip Start to Clip End,
   as specified in the :doc:`Camera settings </render/cameras>`.
Red, Green, Blue
   Single Color Channel visualized as a grayscale image.


Main View
=========

When :kbd:`LMB` / :kbd:`RMB` dragging mouse the color under the cursor is shown in the footer as well the cursor
position and the color values in the RGBA, HSV and Luminance :term:`color space`.


Sidebar Region
==============

Tool
   Displays the settings of the active tool.
Image
   Tools for working with images, see :doc:`/editors/image/image_settings`.
View Tab
   Controls display options, see :doc:`/editors/image/view_tab`.
Scopes
   Displays :doc:`scopes </editors/image/scopes>` visualizing information about the image.
