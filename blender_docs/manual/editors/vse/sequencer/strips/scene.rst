.. _bpy.types.SceneSequence:

***********
Scene Strip
***********

Scene strips are a way to insert the render output of a scene into your sequence.
Instead of rendering out a video, then inserting the video file, you can insert the scene directly.

The strip length will be determined based on the animation settings in that scene.


Options
=======

Use Sequence
   Expand the scenes sequence strips, allowing one scene to reuse another scene's edit
   (instead of taking the render output from the scene).

   This is similar to how :doc:`Meta Strips </editors/vse/sequencer/meta>` work,
   with the added advantage of supporting multiple instances of the same data.
Camera Override
   This can be used to override the scene's camera with any other object.

   It is useful to support switching views within a single scene.
Show Grease Pencil
   Shows :doc:`Grease Pencil </editors/3dview/grease_pencil/index>` in OpenGL preview.
Audio Volume
   Volume of the audio taken from the chosen scene.
Alpha Mode
   Sky
      Fills in a solid background.
   Transparent
      Creates a transparent background.
      This is useful for doing overlays like rendering out Grease Pencil films via the Sequencer.

.. hint::

   It's best not add a scene strip for the scene you are currently editing.
   While this is supported, it can be confusing when changing the start and end frame.
