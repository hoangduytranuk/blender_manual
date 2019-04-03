
************
Introduction
************

.. The UV/Image Editor offers few options to edit images > Compositor texture mode.


Header
======

Image Menu
----------

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
   but will keep the old one open in the UV/Image editor.
Edit Externally
   Using the *Edit Externally* tool Blender will open an external image editor,
   as specified in the *User Preferences* and load in the image to be edited.
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


Controls
--------

Image
   :ref:`Data-block menu <ui-data-block>` used for selecting images.
   When an image has been loaded or created in the UV/Image editor,
   the Image panel appears in the *Properties region*.
   See :doc:`/editors/uv_image/image/image_settings`.

   - Render Result
   - Viewer Node
Pin Image
   Displays current image regardless of selected object.


Multi-Layer
^^^^^^^^^^^

When a rendered image is displayed in the UV/Image Editor,
several new menu items become available.

Slot
   You can save successive renders into the render buffer by selecting a new slot before rendering.
   If an image has been rendered to a slot, it can be viewed by selecting that slot.
   Empty slots appear as blank grids in the UV/Image editor.
   Use the :kbd:`J` and :kbd:`Alt-J` to cycle forwards and backwards through saved renders.
   The *Slot Name* field in the *Display Panel* allows you to rename a slot.
Render Layer
   If you are using :doc:`Render Layers </render/post_process/layers>`,
   use this menu to select which layer is displayed.
Render Pass
   If you are using :doc:`Render Passes </render/cycles/settings/scene/render_layers/passes>`,
   use this menu to select which pass is displayed.


Channels
^^^^^^^^

Draw Channels
   The radio buttons set which channels of the image are displayed.

   RGBA
      Replaces transparent pixels with background checkerboard, denoting the alpha channel.
   RGB
      Draw the colored image, without alpha channel.
   Alpha
      Displays the Alpha channel a grayscale image. White areas are opaque, black areas have an alpha of 0.
   Z-Buffer
      Display the depth from the camera, from Clip Start to Clip End,
      as specified in the :doc:`Camera settings </render/cycles/camera>`.
   Red, Green, Blue
      Single Color Channel visualized as a grayscale image.


Main View
=========

When :kbd:`LMB` dragging mouse the color under the cursor is shown in the footer as well the cursor position and
the color values in the RGBA, HSV and Luminance :term:`color space`.
