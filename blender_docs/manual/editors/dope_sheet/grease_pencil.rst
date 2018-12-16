
*************
Grease Pencil
*************

This Mode allows you adjust the timing of the :doc:`Grease pencil tool's </editors/3dview/grease_pencil/index>`
animated sketches. It is especially useful for animators blocking out shots,
where the ability to re-time blocking is one of the main purposes of the whole exercise.

This mode can be accessed by changing the Dope Sheet editor's *Mode* selector (found beside the menus)
to *Grease Pencil*.

.. figure:: /images/editors_dope-sheet_introduction_overview.png
   :width: 620px


Channels Region
===============

Grease Pencil (light blue)
   The channels' region shows the Grease Pencil data-blocks containing the layers.
   Multiple blocks are used for each area (e.g. one for the 3D View and the UV/Image editor).
Layers (gray)
   These channels contain the keyframes to which
   the :doc:`layers </editors/3dview/grease_pencil/drawing/layers>` are bound.


Header
======

Active Only
   Only show the Grease Pencil blocks attached to the current scene and the objects within it.


Copying Sketches
----------------

It is possible to copy sketches from a layer/layers to other layers
using the *Copy* and *Paste* buttons in the header.
This works in a similar way as the copy/paste tools for keyframes in the *Action Editor*.

Sketches can also be copied from data-block to another using these tools.
It is important to keep in mind that keyframes will only be pasted into selected layers,
so layers will need to be created for the destination areas too.


Main View
=========

The keyframes can be manipulated like any other data in the *Dope Sheet* can be.
Interpolated keyframes (alias breakdowns) are visualized as smaller light blue points.


Insert Keyframe
---------------

Insert Keyframe :kbd:`I` can be used for creating blank Grease Pencil frames at a particular frame.
It will create blank frames if *Additive Drawing* is disabled, otherwise
it will make a copy of the active frame on that layer, and use that.
