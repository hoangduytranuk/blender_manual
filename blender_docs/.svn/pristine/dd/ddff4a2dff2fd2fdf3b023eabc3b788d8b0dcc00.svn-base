
************
Introduction
************

A *Keyframe* is simply a marker of time which stores the value of a property.

For example, a Keyframe might define that the horizontal position of a cube is at 3m on frame 1.

The purpose of a Keyframe is to allow for interpolated animation, meaning, for example,
that the user could then add another key on frame 10, specifying the cube's horizontal position at 20m,
and Blender will automatically determine the correct position of the cube for all the frames between frame 1 and 10
depending on the chosen interpolation method (e.g. Linear, Bézier, Quadratic, etc.).


Visualization
=============

There are some important visualization features in the 3D Views that can help animation.

When the current frame is a keyframe for the current active object, the name of this object
(shown in the upper left corner of the 3D Views) turns yellow.

.. figure:: /images/animation_keyframes_introduction_visualization.png

   Bottom: Current frame isn't a keyframe. Top: Current frame is a keyframe for Cube.


.. _keyframe-type:

Keyframe Types
==============

For visually distinguishing regular keyframes from different animation events or
states (extremes, breakdowns, or other in-betweens)
there is the possibility of applying different colors on them for visualization.

.. figure:: /images/animation_keyframes_introduction_types.png

   Left: not selected; Right: selected.

Keyframe (white / yellow diamond)
   Normal keyframe.
Breakdown (small cyan diamond)
   Breakdown state. e.g. for transitions between key poses.
Moving Hold (dark gray / orange diamond)
   A keyframe that adds a small amount of motion around a holding pose.
   In the Dope Sheet it will also display a bar between them.
Extreme (big pink diamond)
   An 'extreme' state, or some other purpose as needed.
Jitter (tiny green diamond)
   A filler or baked keyframe for keying on ones, or some other purpose as needed.


.. _keyframe-handle-display:

Handles & Interpolation Display
===============================

Dope Sheet can display the Bézier handle type associated with the keyframe,
and mark segments with non-Bézier interpolation.
This facilitates basic editing of interpolation without the use of the Graph Editor.

.. figure:: /images/animation_keyframes_introduction_interpolation.png

   Top: summary; Middle: Bézier; Bottom: linear.

The icon shape represents the type of the :ref:`Bézier Handles <editors-graph-fcurves-settings-handles>`
belonging to the keyframe.

.. list-table::

   * - Circle
     - Auto Clamped (default)
   * - Circle With Dot
     - Automatic
   * - Square
     - Vector
   * - Clipped Diamond
     - Aligned
   * - Diamond
     - Free

If the handles of a keyframe have different types,
or in case of summary rows representing multiple curves,
out of the available choices the icon that is furthest down the list is used.
This means that if a grouped row uses a circle icon,
it is guaranteed that none of the grouped channels have a non-auto key.

Horizontal green lines mark the use of non-Bézier :ref:`Interpolation <editors-graph-fcurves-settings-interpolation>`.
The line is dimmed in summary rows if not all grouped channels have the same interpolation.

Display of this information can be disabled via the *Show Handles and Interpolation*
option of the Dope Sheet's :ref:`View Menu <dope-sheet-view-menu>`.
