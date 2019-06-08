
************
Introduction
************

In addition to modeling and animation, Blender can be used to edit video.
There are two possible methods for this, one being the :doc:`Compositor </compositing/introduction>`.
However, this chapter describes the other, the Video Sequence Editor (VSE), sometimes shortened to just "Sequencer".
The Sequencer within Blender is a complete video editing system that allows you to combine multiple
video channels and add effects to them. You can use these effects to create powerful video edits,
especially when you combine it with the animation power of Blender!

To use the VSE, you load multiple video clips and lay them end-to-end (or in some cases, overlay them),
inserting fades and transitions to link the end of one clip to the beginning of another.
Finally, you can add audio and synchronize the timing of the video sequence to match it.

.. figure:: /images/editors_vse_introduction_screen-layout.png
   :width: 620px

   Default Video Editing screen layout.


View Types
==========

The Video Sequence Editor has three view types for the main view.

The View Types toggles in the header allow you to change the view of the VSE.
When the first button is toggled only the Sequencer is displayed (the default).
The second button displays only the Preview region, and
the third button displays both the Sequencer and the Preview.

.. note::

   By default the Sequencer is enabled, however, it can be disabled
   in the :ref:`render-output-postprocess`.

/scratch/src/manual/manual/editors/vse/introduction.rst:35:
