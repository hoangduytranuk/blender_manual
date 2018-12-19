
**********
Properties
**********

Scene Preview/Render
====================

It allows you to control how the images of :doc:`Scene Strips </editors/vse/sequencer/strips/scene>`
are displayed in the preview.

OpenGL Preview
   Use a quick OpenGL preview (see :doc:`OpenGL render </render/opengl>` for more on this subject),
   otherwise a full render is used, which can be very slow.

   Sequencer Preview Shading
      Method for rendering OpenGL renders.
      See the 3D View's :ref:`view3d-viewport-shading` options.
   Textured Solid
      Display textures even when in solid mode.

   Settings used by OpenGL Previews:

   - The anti-alias setting from the active scene is used for all scenes.
   - The alpha setting is taken from each scene strip *Alpha Mode* option.


View Settings
=============

Show Overexposed
   Shows overexposed (bright white) areas using a zebra pattern.
   The threshold can be adjust with the slider.
Proxy Render Size
   Size to display proxies at in the preview region.
   Using a smaller preview size will increase speed.


Safe Areas
==========

Shows guides used to position elements to ensure that
the most important parts of the video can be seen across all screens.

.. seealso::

   See :ref:`Safe Areas <camera-safe-areas>` in the camera docs.


Grease Pencil
=============

Allows you to use :doc:`Grease Pencil </editors/3dview/grease_pencil/index>` in the Sequencer.
