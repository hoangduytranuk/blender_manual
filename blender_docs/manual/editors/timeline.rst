.. |first| unicode:: U+023EE
.. |last|  unicode:: U+023ED
.. |rewind| unicode:: U+025C0
.. |play|   unicode:: U+025B6
.. |previous| unicode:: U+023EA
.. |next|     unicode:: U+023E9
.. |pause| unicode:: U+023F8

.. _bpy.types.SpaceTimeline:
.. _bpy.ops.time:

***************
Timeline Editor
***************

The *Timeline* editor, identified by a clock icon, is not much of an editor,
but more used to view information and control animation playback.

.. figure:: /images/editors_timeline_interface.png

   The Timeline.

The *Timeline* is one of an animator's most useful tools as it can give a broad overview of a scene's animation.
The Timeline can communicate the current time frame, either in frames or in seconds,
where the keyframes are of the active object, the start and end frames of your animation, markers, etc.

The *Timeline* has *Player Controls*, to play, pause the animation,
and to skip through parts of the scene.

It also has some tools for *Keyframes*, *Keying Sets*, and *Markers*.


Main View
=========

The main *Timeline* region displays the animation frames over time.

.. figure:: /images/editors_timeline_main.png

   Timeline main view.


Adjusting the View
------------------

The *Timeline* can be panned by holding :kbd:`MMB`,
then dragging the area left or right.

You can zoom the *Timeline* by using :kbd:`Ctrl-MMB`, the mouse :kbd:`Wheel`,
or pressing :kbd:`NumpadMinus` and :kbd:`NumpadPlus`.


Time Cursor
-----------

The *Time Cursor* is the green line, it is used to set and display the current time frame.

.. figure:: /images/editors_timeline_cursor.png

   Time Cursor.

The *Time Cursor* can be set or moved to a new position by pressing or
holding :kbd:`LMB` in the Timeline editor.

The current frame or second can be displayed on the *Time Cursor*,
check the View menu for settings.

The *Time Cursor* can be moved in steps by pressing :kbd:`Left` or :kbd:`Right`,
or in steps of 10 frames by pressing :kbd:`Shift-Up` or :kbd:`Shift-Down`.


Playback/Rendering Range
------------------------

By default, the *Playback/Rendering Range* (Frame Start 1 to Frame End 200)
is a lighter shade of gray. The start and end frame can be set to the *Time Cursor*
by pressing :kbd:`S` or :kbd:`E`.
The *Playback Range* can also be set by pressing :kbd:`P` then drawing a box.


Keyframes
---------

For the active and selected objects, keyframes are displayed as a yellow line.
For *Armatures*, the object keyframes and the pose bones keyframes are drawn.

*Only Selected Channels* can be enabled. :menuselection:`Timeline --> View --> Only Selected Channels`.
For *Armatures*, this will draw the object keyframes,
and the keyframes for the active and selected pose bones.


Markers
-------

See the :doc:`Markers page </animation/markers>` for more information.

Header
======

Popovers
--------

.. _timeline-playback:

Playback Popover
^^^^^^^^^^^^^^^^

The *Playback Popover* contains options controlling animation playback.

Synchronize Playback
   .. figure:: /images/editors_timeline_red-fps.png
      :figwidth: 109px
      :align: right

      3D View red FPS.

      60:54.75

   When you play an animation, the FPS is displayed at the top left of the 3D View.
   If the scene is detailed and playback is slower than the set
   *Frame Rate* (see :ref:`render-tab-dimensions`),
   these options are used to synchronize the playback.

   No Sync
      Do not sync, play every frame.
   Frame Dropping
      Drop frames if playback is too slow.
   AV-sync
      (Audio/Video Synchronization). Sync to audio clock, dropping frames if playback is slow.
Audio Scrubbing
   If your animation has sound, this option plays bits of the sound wave
   while you move the time cursor with :kbd:`LMB` or keyboard arrows (like a moving playhead).
Mute Audio
   Mute the sound from Sequence Editors.
Subframes
   Display and allow changing the current scene sub-frame.
Limit Playhead to Frame Range
   Don't allow selecting frames outside of the playback range using the mouse.
Follow Playhead
   Animation editors can be setup to always follow the time indicator as animation is being played back.
   Following will be done when animating and changing frame.
   When the cursor reaches the end of the screen, the next range of frames of the same width will be displayed.
Active Editor Only
   While playing, updates the Timeline, if Animation Editors and All 3D View Editors disabled.
All 3D View Editors
   While playing, updates the 3D View and the Timeline.
Animation Editors
   While playing, updates the Timeline, Dope Sheet, Graph Editor, Video Sequence Editor.
Property Editors
   When the animation is playing, this will update the property values in the UI.
Image Editors
   The UV/Image editor in Mask mode.
Sequencer Editors
   While playing, updates the Video Sequence Editor.
Node Editors
   While playing, updates the Node properties for the Node Editor.
Clip Editors
   While playing, updates the Movie Clip Editor.

.. _timeline-keying:

Keying Popover
^^^^^^^^^^^^^^

The *Keying Popover* contains options that affect keyframe insertion.

Active Keying Set
   .. figure:: /images/editors_timeline_keying-sets.png
      :align: right

      Timeline Keying Sets.

   *Keying Sets* are a set of keyframe channels in one.
   They are made so the user can record multiple properties at the same time.
   With a keying set selected, when you insert a keyframe,
   Blender will add keyframes for the properties in the active *Keying Set*.
   There are some built-in keying sets, *LocRotScale*, and also custom keying sets.
   Custom keying sets can be defined in the panels
   :menuselection:`Properties --> Scene --> Keying Sets + Active Keying Set`.

   Insert Keyframes (plus icon)
      Insert keyframes on the current frame for the properties in the active *Keying Set*.
   Delete Keyframes (minus icon)
      Delete keyframes on the current frame for the properties in the active *Keying Set*.

New Keyframe Type
   :ref:`keyframe-type` on insertion.

Auto-Keyframing Mode
   This controls how the Auto Keyframe mode works.
   Only one mode can be used at a time.

   Add & Replace
      Add or Replace existing keyframes.
   Replace
      Only Replace existing keyframes.

Auto Keying Set (two keys icon)
   When enabled *Auto Keyframe* will insert new keyframes for the properties in the active *Keying Set*.

Layered Recording
   Adds a new NLA Track and strip for every loop/pass made over the animation to allow non-destructive tweaking.

Cycle-Aware Keying
   When inserting keyframes into :ref:`trivially cyclic curves <bpy.types.FModifierCycles>`, special handling
   is applied to preserve the cycle integrity (most useful while tweaking an established cycle):

   * If key insertion is attempted outside of the main time range of the cycle, it is remapped back inside the range.
   * When overwriting one of the end keys, the other one is updated appropriately.


Menus
-----

.. _timeline-view-menu:

View Menu
^^^^^^^^^

The *View Menu* controls what you see, and what it looks like.

Show Seconds :kbd:`Ctrl-T`
   Whether to show the time in the X axis and the *Time Cursor* as
   frames (based on the FPS) or as seconds.
Lock Time to Other Windows
   It synchronizes the horizontal panning and scale of the current editor
   with the other editors (Graph, Dope Sheet, NLA) when this option is set.
   That way you always have these editors showing an identical part of the time you work on.
Show Frame Number Indicator
   This will draw the current frame or seconds on the *Time Cursor*.
Only Keyframes from Selected Channels
   For *Armatures*, this will draw the object keyframes,
   and the keyframes for the active and selected pose bones.
Cache
   Show Cache
      Show all enabled types.

      Softbody, Particles, Cloth, Smoke, Dynamic Paint, Rigid Body.

   .. figure:: /images/editors_timeline_cache.png

      Timeline Cache.

View All :kbd:`Home`
   Maximize the area based on the Animation Range.
View Frame :kbd:`Numpad0`
   Centers the Timeline to the Time cursor.

.. removed in 2.8

Bind Camera to Markers :kbd:`Ctrl-B`
   This is used to switch cameras during animation.
   It binds the active camera to the selected markers.
   First select a camera. Then select the marker(s). Then use the tool.


Markers Menu
^^^^^^^^^^^^

:doc:`Markers </animation/markers>` are used to denote frames with key points or significant events
within an animation. Like with most animation editors, markers are shown at the bottom of the editor.

.. figure:: /images/editors_graph-editor_introduction_markers.png

   Markers in animation editor.

For descriptions of the different marker tools see :ref:`Editing Markers <animation-markers-editing>`.


.. _animation-editors-timeline-headercontrols:

Header Controls
---------------

The Timeline header controls.

.. figure:: /images/editors_timeline_header.png

   Timeline header controls.

   \1. Range Control, 2. Frame Control, 3. Player Control,
   \4. Synchronize Playback, 5. Keyframe Control.


Range Control
^^^^^^^^^^^^^

Use Preview Range (clock icon)
   This is an alternative range used to preview animations.
   This works for the UI playback, this will not work for rendering an animation.
   See :ref:`graph-preview-range`.


Frame Control
^^^^^^^^^^^^^

Start Frame
   The start frame of the animation/playback range.
End Frame
   The end frame of the animation/playback range.
Current Frame :kbd:`Alt-Wheel`
   The current frame of the animation/playback range.
   Also the position of the *Time Cursor*.


Player Control
^^^^^^^^^^^^^^

These buttons are used to set, play, rewind, the *Time Cursor*.

.. figure:: /images/editors_timeline_player-controls.png
   :align: right

   Player controls.

Jump to start (|first|) :kbd:`Shift-Ctrl-Down`, :kbd:`Shift-Left`
   This sets the cursor to the start of frame range.
Jump to previous keyframe (|previous|) :kbd:`Down`
   This sets the cursor to the previous keyframe.
Rewind (|rewind|) :kbd:`Shift-Alt-A`
   This plays the animation sequence in reverse.
   When playing the play buttons switch to a pause button.
Play (|play|) :kbd:`Alt-A`
   This plays the animation sequence.
   When playing the play buttons switch to a pause button.
Jump to next keyframe (|next|) :kbd:`Up`
   This sets the cursor to the next keyframe.
Jump to end (|last|) :kbd:`Shift-Ctrl-Up`, :kbd:`Shift-Right`
   This sets the cursor to the end of frame range.
Pause (|pause|) :kbd:`Alt-A`
   This stops the animation.


.. Move to animation?
.. _animation-editors-timeline-autokeyframe:

Keyframe Control
^^^^^^^^^^^^^^^^

Auto Keyframe
   .. figure:: /images/editors_timeline_keyframes-auto.png
      :align: right

      Timeline Auto Keyframe.

   The record button (red dot) enables something called *Auto Keyframe*:
   It will add and/or replace existing keyframes for the active object when you transform it in the 3D View.

   For example, when enabled, first set the *Time Cursor* to the desired frame,
   then move an object in the 3D View, or set a new value for a property in the UI.

   When you set a new value for the properties,
   Blender will add keyframes on the current frame for the transform properties.
   Other use cases are :ref:`Fly/Walk Mode <3dview-walk-fly>` to record the walk/flight path
   and :ref:`Lock Camera to View <3dview-lock-camera-to-view>` to record the navigation in camera view.

   .. note::

      Note that *Auto Keyframe* only works for transform properties (objects and bones),
      in the 3D Views (i.e. you can't use it e.g. to animate the colors of a material in the Properties editor...).

