
************
Introduction
************

.. figure:: /images/editors_dope-sheet_introduction_overview.png
   :width: 620px

   The Dope Sheet.

The Dope Sheet gives the animator a "birds-eye-view" of everything occurring within a scene.
It contains a collection of animation editors.

Classical hand-drawn animators often made a chart, showing exactly when each drawing,
sound and camera move would occur, and for how long. They nicknamed this the "dope sheet".
While CG foundations dramatically differ from classical hand-drawn animation,
Blender's *Dope Sheet* inherits a similar directive.


Dope Sheet Modes
================

.. figure:: /images/editors_dope-sheet_introduction_modes.png

   Dope Sheet modes.

While the Dope Sheet Mode allow you to edit multiple actions at once,
the other ones are dedicated to view and edit specific data-blocks used in different context of animation.

- Dope Sheet
- :doc:`Action Editor </editors/dope_sheet/action>`
- :ref:`Shape Key Editor <dope-sheet-shape-key>`
- :doc:`Grease Pencil </editors/dope_sheet/grease_pencil>`
- :ref:`Mask <dope-sheet-mask>`
- Cache File: Alembic Todo 2.78.


Interface
=========

The *Dope Sheet Editor* interface is somewhat similar to the *Graph Editor*
one, it is divided in three regions:

.. figure:: /images/editors_dope-sheet_action_editor.png
   :width: 670px

   The Action Editor with object channels.


Header
------

Here you find the menus, a first block of controls related to the editor "mode",
a second one concerning the action data-blocks, and a few other tools
(like the copy/paste buttons, and snapping type).

Summary
   Toggles the "Dope Sheet Summary" channel at the top of the `Channels Region`_.
   This is used to give an overview of all the channels by combining all the actions into one channel.


View Menu
^^^^^^^^^

Sync Markers
   Sync Markers with keyframe edits.

Show Handles and Interpolation
   Instead of drawing all keyframes as diamonds, different icons are used to show the Bézier handle type.
   When curves use a different interpolation type, a line is drawn between keys to highlight that.

   If the two handles of a key have different handle types, or the icon represents multiple curves,
   the "least automatic" handle type is chosen, with the ordering determined as
   *Free* -- *Aligned* -- *Vector* -- *Automatic* -- *Auto Clamped*.
Show Extremes
   Detect keys where the curve changes direction based on comparing with the adjacent key values,
   and display that by changing the keyframe icons to resemble an arrow.
   A muted version of the icon is used if the curve overshoots the extreme,
   or for groups with different results for contained curves.

See Graph editor's :ref:`graph-view-menu`.


Markers Menu
^^^^^^^^^^^^

:doc:`Markers </animation/markers>` are used to denote frames with key points or significant events
within an animation. Like with most animation editors, markers are shown at the bottom of the editor.

.. figure:: /images/editors_graph-editor_introduction_markers.png

   Markers in animation editor.

For descriptions of the different marker tools see :ref:`Editing Markers <animation-markers-editing>`.


Key Menu
^^^^^^^^

Keyframe Type :kbd:`R`
   Sets the :ref:`keyframe-type` of the selected keyframes.

See :doc:`F-Curve </editors/graph_editor/fcurves/index>`.


Main Region
-----------

It contains the keyframes for all visible action channels.
As with the other "time" editor, the X axis represents time.
The Y axis has no mean in itself, unlike with the *Graph Editor*, it is a "stack" of action channels.

Each one being shown as a horizontal colored strip (of a darker shade "during" the animated/keyed period).
On these channel strips lay the keyframes, visualized as light gray (unselected) or yellow (selected) diamonds.

One of the key feature of this editor is that it allow you to visualize immediately which channel (i.e. F-Curve)
is *really* affected. When the value of a given channel does not change at all between two neighboring keyframes
("long keyframes"), a gray (unselected) or yellow (selected) bar is drawn between them.
Similar bars are drawn between keyframes tagged as moving hold.


Channels Region
---------------

.. _fig-dope-sheet-action:

.. figure:: /images/editors_dope-sheet_introduction_action-editor-sliders.png

   The Action editor's channels region.

See :doc:`/editors/graph_editor/channels`.
