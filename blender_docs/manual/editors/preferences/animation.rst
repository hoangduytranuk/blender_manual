
*********
Animation
*********

The *Animations* section lets you manage settings related to :doc:`Animation </animation/index>`.
This includes how editors look and also some different tools properties.

.. figure:: /images/editors_preferences_section_animation.png

   Blender Preferences Animation section.


Timeline
========

These settings control things in the :doc:`Timeline </editors/timeline>`.

Allow Negative Frame
   Playhead can be set to negative frames with mouse or keyboard.
   When using *Use Preview Range*, this also allows playback.
Minimum Grid Spacing
   The minimum number of pixels between grid lines.
TimeCode Style
   Format of Time Codes displayed when not displaying timing in terms of frames.
   The format uses '+' as a separator for sub-second frame numbers,
   with left and right truncation of the timecode as necessary.
Zoom To Frame Type
   Defines what time range (around the cursor) will be displayed
   when the *View Frame* :kbd:`Numpad0` is performed.

   Keep Range
      The currently displayed time range is preserved.
   Seconds
      The number of seconds specified in the *Zoom Seconds* field will be shown around the cursor.
   Keyframes
      The number of animation keyframes defined in the *Zoom Keyframes* field will be shown around the cursor.


Keyframes
=========

These settings control :doc:`Keyframes </animation/keyframes/index>`
which are the building blocks for animations.

Visual Keying
   When an object is using constraints, the object property value does not actually change.
   *Visual Keying* will add keyframes to the object property,
   with a value based on the visual transformation from the constraint.
Only Insert Needed
   This will only insert keyframes if the value of the property is different.


Auto-Keyframing
---------------

Auto Keyframing
   Enables *Auto Keyframe* by default for new scenes.
Show Auto Keying Warning
   Displays a warning at the top right of the *3D View*, when moving objects, if *Auto Keyframe* is on.
Only Insert Available
   This will only add keyframes to channels of F-curves that already exist.

.. seealso::

   Learn more about :ref:`Auto-Keyframing <animation-editors-timeline-autokeyframe>`.


F-Curves
========

These settings control how :doc:`F-Curves </editors/graph_editor/fcurves/index>`
look and their default behavior.

F-Curve Visibility
   Opacity that unselected :doc:`F-Curves </editors/graph_editor/fcurves/index>`
   stand out from the *Graph Editor*.
Interpolation
   Controls the default :ref:`Interpolation <editors-graph-fcurves-settings-interpolation>`
   for newly created keyframes.
Default Handles
   Controls the default :ref:`Handle <editors-graph-fcurves-settings-handles>` for newly created F-curves.
XYZ to RGB
   Color for X, Y or Z animation curves (location, scale or rotation)
   is the same as the color for the X, Y and Z axis.
