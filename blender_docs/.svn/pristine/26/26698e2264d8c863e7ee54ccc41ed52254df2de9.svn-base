
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
(shown in the bottom left corner of the 3D Views) turns yellow.

.. figure:: /images/animation_keyframes_introduction_visualization.png

   Bottom: Current frame at 0. Top: Current frame is a keyframe for Cube.


.. _keyframe-type:

Keyframe Types
==============

For visually distinguish regular keyframes from different animation events or
states (extremes, breakdowns, or other in-betweens)
there is the possibility of applying different colors on them for visualization.

Keyframe (yellow diamond)
   Normal keyframe.
Breakdown (cyan small diamond)
   Breakdown state. e.g. for transitions between key poses.
Moving Hold (slight orange diamond)
   A keyframe that adds a small amount of motion around a holding pose.
   In the Dope Sheet it will also draw a bar between them.
Extreme (red big diamond)
   An 'extreme' state, or some other purpose as needed.
Jitter (green tiny diamond)
   A filler or baked keyframe for keying on ones, or some other purpose as needed.
