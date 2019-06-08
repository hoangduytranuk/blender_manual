
************
Introduction
************

The Image Editor is where you can view/edit 2D assets like images or textures.

.. figure:: /images/editors_uv-image_introduction_main.png

   Image Editor with a test grid texture.


Header
======

View
   Tools for controlling how the content is displayed in the editor.
   See :doc:`/editors/image/navigating`.
Image
   :ref:`Data-block menu <ui-data-block>` used for selecting images.
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
      :doc:`/editors/movie_clip_editor/masking/index`.


Multi-Layer
-----------

When a rendered image is displayed in the Image Editor,
several new menu items become available.

Slot
   You can save successive renders into the render buffer by selecting a new slot before rendering.
   If an image has been rendered to a slot, it can be viewed by selecting that slot.
   Empty slots appear as blank grids in the Image editor.
   Use the :kbd:`J` and :kbd:`Alt-J` to cycle forwards and backwards through saved renders.
   The *Slot Name* field in the *Display Panel* allows you to rename a slot.
Render Layer
   If you are using :doc:`Render Layers </render/layers/index>`,
   use this menu to select which layer is displayed.
Render Pass
   If you are using :doc:`Render Passes </render/layers/passes>`,
   use this menu to select which pass is displayed.


Display Channels
----------------

The radio buttons set which channels of the image are displayed.

RGBA
   Replaces transparent pixels with background checkerboard, denoting the alpha channel.
RGB
   Draw the colored image, without alpha channel.
Alpha
   Displays the Alpha channel a grayscale image. White areas are opaque, black areas have an alpha of 0.
Z-Buffer
   Display the depth from the camera, from Clip Start to Clip End,
   as specified in the :doc:`Camera settings </render/camera>`.
Red, Green, Blue
   Single Color Channel visualized as a grayscale image.


Main View
=========

When :kbd:`LMB` dragging mouse the color under the cursor is shown in the footer as well the cursor position and
the color values in the RGBA, HSV and Luminance :term:`color space`.


Sidebar Region
==============

Tool
   Todo.
Image
   Tools for working with images see :doc:`/editors/image/image_settings`.
View Tab
   Controls display options see :doc:`/editors/image/view_tab`.
