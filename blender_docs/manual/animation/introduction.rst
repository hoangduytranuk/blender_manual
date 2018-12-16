
************
Introduction
************

Animation is making an object move or change shape over time.
Objects can be animated in many ways:

Moving as a whole object
   Changing their position, orientation or size in time;
Deforming them
   Animating their vertices or control points;
Inherited animation
   Causing the object to move based on the movement of another object (e.g. its parent, hook, armature, etc.).

In this chapter, we will cover the first two,
but the basics given here are actually vital for understanding the following chapters as well.

Animation is typically achieved with the use of :doc:`keyframes </animation/keyframes/introduction>`.


.. seealso:: Related Sections

   The :doc:`Rigging section </rigging/index>`, :doc:`Physical Simulation </physics/introduction>`
   and :doc:`Motion Tracking </editors/movie_clip_editor/index>`.


.. _animation-state-colors:

State Colors
============

.. figure:: /images/animation_introduction_state-colors.png

   State colors of properties.

Properties have different colors and menu items for different states.

.. object origin, 3D View overlay

.. list-table::

   * - Gray
     - Default
   * - Yellow
     - Keyframes
   * - Green
     - Animated
   * - Purple
     - Driver
