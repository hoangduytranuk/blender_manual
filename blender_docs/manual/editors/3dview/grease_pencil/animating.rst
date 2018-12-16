.. (TODO) This page should be a general workflow page.

******************
Animating Sketches
******************

You can use Grease Pencil to create 2D animations (e.g. in flipbook style) and
mixing it with 3D objects and composition.

Sketches are stored on the frame that they were drawn on, as a separate drawing
(only on the layer that they exist on). A keyframe is automatically added per layer.
Each drawing is visible until the next drawing for that layer is encountered.
The only exception to this is the first drawing for a layer,
which will also be visible before the frame it was drawn on.

Therefore, it is simple to make a pencil-test/series of animated sketches:

#. Go to first relevant frame. Draw.
#. Jump to next relevant frame. Draw some more.
#. Keep repeating process, and drawing until satisfied. Voilà! Animated sketches.

.. (todo <2.8 add) keyframes, on properties.

.. seealso::

   Grease Pencil mode in the :doc:`Dope Sheet </editors/dope_sheet/grease_pencil>` editor.


Compositing
===========

The Grease pencil layers create a pass inside :doc:`OpenGL </render/opengl>` render result.
This result can be exported to ``EXR multilayer`` and used in composition.

ToDo add.


Example
=======

.. youtube:: vSD5mN7LT_g
