
************
Introduction
************

The Movie Clip Editor has two main purposes, it can be used for tracking or masking movies.
The empty editor looks like the image below.

.. figure:: /images/editors_movie-clip-editor_introduction_interface.png

   Movie Clip Editor interface.


Header
======

Clip Menu
---------

- Open Clip :kbd:`Alt-O`


Controls
--------

Movie Clip
   :ref:`Data-block menu <ui-data-block>` used for add a movie file.
   Both movie files and image sequences can be used in the Clip editor.
   When a movie clip is loaded into the Clip editor, extra panels are displayed in the interface.

.. figure:: /images/editors_movie-clip-editor_introduction_example.png

   Movie Clip Editor with an opened clip.

Modes
   - :doc:`Motion Tracking </editors/movie_clip_editor/tracking/index>`
   - :doc:`Masking </editors/movie_clip_editor/masking/index>`

Pivot Point
   See :doc:`Pivot Points </scene_layout/object/editing/transform/control/pivot_point/index>`.
Proportional Edit
   See :doc:`Proportional Edit </scene_layout/object/editing/transform/control/proportional_edit>`.


Sidebar Region
==============

Footage Settings
   See :doc:`/editors/image/image_settings`.


Main View
=========

Mini Timeline
-------------

When a clip is loaded a Timeline is shown at bottom of the Preview.
It expands over the full area limited by the animation range.
You can move the Time Cursor by dragging with :kbd:`LMB`.

The Timeline is composed of the following visual elements:

- Green line: Time Cursor
- Yellow: Motion track
- Yellow line: Keyframe
- Orange line: Shape keyframe
- Purple: Prefetched frames
- Light green line: Solve start/end keyframe
