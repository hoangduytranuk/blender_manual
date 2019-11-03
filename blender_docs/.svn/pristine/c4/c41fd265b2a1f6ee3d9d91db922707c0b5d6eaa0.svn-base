
************
Introduction
************

The NLA editor, short for Non-Linear Animation, can manipulate and repurpose :doc:`/animation/actions`,
without the tedium of handling keyframes. It is often used to make broad,
significant changes to a scene's animation, with relative ease.
It can also repurpose, chain together a sequence of motions, and "layered" actions, which make it easier to organize,
and version-control your animation.


Header
======

View Menu
---------

Realtime Updates
   When transforming NLA-strips the changes to the animation is propagated to other views.
Show Control F-Curves
   Overlays a graph of the NLA-strip's influence on top of the strip.
Show Local Markers
   Shows action-local markers on the strip, this is useful when synchronizing time across strips.

Set Preview Range
   Selecting a preview range by dragging in the NLA Editor.
Clear Preview Range
   Unset the preview range
Auto Select Preview Range
   Automatically select the preview range based on the range of keyframes.

.. seealso:: See Timeline's :ref:`timeline-view-menu`.


Select Menu
-----------

All
   Select all NLA-strips.
None
   Deselect all NLA-strips.
Invert
   Invert the current selection of NLA-strips.
Box Select
   Select NLA-strips by drawing a box. All NLA-strips that intersects the box
   will be added to the current selection.
Border Axis Range
   Select NLA-strips by drawing a box. All NLA-strips that intersects the frames
   of the drawn box will be added to the current selection.
Before Current Frame
   Select all NLA-strips before the current frame.
After Current Frame
   Select all NLA-strips after the current frame.


Markers Menu
------------

:doc:`Markers </animation/markers>` are used to denote frames with key points or significant events
within an animation. Like with most animation editors, markers are shown at the bottom of the editor.

.. figure:: /images/editors_graph-editor_introduction_markers.png

   Markers in animation editor.

For descriptions of the different marker tools, see :ref:`Editing Markers <animation-markers-editing>`.


Edit Menu
---------

Transform
   Move
      Move the selected NLA-strips in time or to different NLA-track.
   Extend
      Extend the selected NLA-strips.
   Scale
      Scale the selected NLA-strips.
Snap
   Current Frame
      Move the start of selected NLA-strips to the current frame.
   Nearest Frame
      Move the start of the selected NLA-strips to the nearest frame.
   Nearest Second
      Move the start of the selected NLA-strips to the nearest second.
   Nearest Marker
      Move the start of the selected NLA-strips to the nearest marker.

Duplicate
   Make a copy of the selected NLA-strips.

Linked Duplicate
   Make a shallow copy of the selected NLA-strips.
Split Strips
   NLA-Split the selected strips into two NLA-strips. The split happens at the current frame.
Delete Strips
   Delete selected NLA-Strips.
Toggle Muting
   Mute or unmute the selected NLA-strips. Muted NLA-strips will not influence the animation.
Apply Scale
   Apply the scale of the selected NLA-strips to their referenced Actions.

Clear Scale
   Reset the scaling of the selected NLA-strips
Sync Action Length
   Synchronize the length of the action to the length used in the NLA-strip.
Make Single User
   This tool ensures that none of the selected strips use an action
   which is also used by any other strips.
Swap Strips
   Swap the order of the selected NLA-strips in their NLA-track.
Move Strips Up
   Move selected NLA-strips a track up if there is room.
Move Strips Down
   Move selected NLA-strips a track down if there is room.
Track Ordering
   To Top
      Move selected track to the top of the tracks.
   Up
      Move selected track one track up.
   Down
      Move selected track one track down.
   To Bottom
      Move selected tracks to the bottom of the tracks.

Remove Empty Animation Data
   Remove Animation Data from selected objects when they don't contain any animation.
Start Editing Stashed Action
   It will enter and exit Tweak Mode as usual, but will also make sure that the action can be edited in isolation
   (by flagging the NLA track that the action strip comes from as being "solo").
   This is useful for editing stashed actions, without the rest of the NLA Stack interfering.
Start Tweaking Strips Actions
   The contents of Action strips can be edited, but you must be in *Tweak Mode* to do so.
   The keyframes of the action can then be edited in the Dope Sheet.


Add
---

Add Action strip
   Add an NLA-strip referencing an Action to the active track.
Add Transition
   Add an NLA-strip to create a transition between a selection of two adjacent NLA-strips.
Add Sound Strip
   Add an NLA-strip controlling when the Speaker object plays its sound clip.

Add Meta-Strip
   Group selected NLA-strips into a meta strip.
   A meta strip will group the selected NLA-strips of the same NLA-track.
Remove Meta-Strip
   Ungroup selected Meta strips.

Add Tracks
   Add a new NLA-Track on top of the selected object.
Add Track Above Selected
   Add a new NLA-Track just above the selected NLA-track.
Include Selected Objects
   Let the selected objects appear in the NLA Editor. This is done by adding
   an empty animation data object to the selected object.
