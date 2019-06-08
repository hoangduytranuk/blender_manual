
**********
Navigation
**********

.. _prefs-input-orbit-style:

Orbit & Pan
===========

Orbit Method
   Select how Blender works when you rotate the 3D View by default when holding :kbd:`MMB`.

   Turntable
      Rotates the view keeping the horizon horizontal.

      This behaves like a potter's wheel or record player where you have two axes of rotation available,
      and the world seems to have a better definition of what is "Up" and "Down" in it.

      The drawback to using the *Turntable* style is that you lose some flexibility when working with your objects.
      However, you gain the sense of "Up" and "Down" which can help if you are feeling disoriented.
   Trackball
      Is less restrictive, allowing any orientation.

Orbit Around Selection
   The selected object (bounding box center) becomes the rotation center of the viewport.
   When there is no selection the last selection will be used.

   .. hint::

      This may seem ideal behavior.
      However, it can become problematic with larger objects such as a terrain-mesh,
      where the center is not necessarily your point of interest.

.. _prefs-interface-auto-perspective:

Auto Perspective
   Automatically to perspective Top/Side/Front view after using User Orthographic.
   When disabled, Top/Side/Front views will retain Orthographic or Perspective view
   (whichever was active at the time of switching to that view).

.. _prefs-auto-depth:

Auto Depth
   Use the depth under the mouse to improve view pan, rotate, zoom functionality.
   Useful in combination with *Zoom To Mouse Position*.

Smooth View
   Length of time the animation takes when changing the view with the numpad
   (Top/Side/Front/Camera...). Reduce to zero to remove the animation.
Rotation Angle
   Rotation step size in degrees, when :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`,
   or :kbd:`Numpad2` are used to rotate the 3D View.


Zoom
====

Zoom Method
   Choose your preferred style of zooming in and out with :kbd:`Ctrl-MMB`.

   Scale
      *Scale* zooming depends on where you first click in the view.
      To zoom out, hold :kbd:`Ctrl-MMB` while dragging from the edge of the screen towards the center.
      To zoom in, hold :kbd:`Ctrl-MMB` while dragging from the center of the screen towards the edge.
   Continue
      The *Continue* zooming option allows you to control the speed
      (and not the value) of zooming by moving away from the initial click point with :kbd:`Ctrl-MMB`.
      Moving up from the initial click point or to the right will zoom out,
      moving down or to the left will zoom in. The further away you move,
      the faster the zoom movement will be.
      The directions can be altered by the *Vertical* and *Horizontal* radio buttons and
      the *Invert Zoom Direction* option.
   Dolly
      *Dolly* zooming works similarly to *Continue* zooming except that zoom speed is constant.
Zoom Axis
   The axis of the :kbd:`MMB` to use for zooming.

   Vertical
      Moving up zooms out and moving down zooms in.
   Horizontal
      Moving left zooms in and moving right zooms out.
Invert Zoom Direction
   Inverts the Zoom direction for *Dolly* and *Continue* zooming.
Invert Wheel Zoom Direction
   Inverts the direction of the mouse wheel zoom.

.. _prefs-zoom-mouse-pos:

Zoom to Mouse Position
   When enabled, the mouse pointer position becomes the focus point of zooming instead of the 2D window center.
   Helpful to avoid panning if you are frequently zooming in and out.


Walk & Fly
==========

View Navigation
   The default navigation mode for :kbd:`Shift-F` in the 3D View.

   Walk
      TODO 2.8.
   Fly
      TODO 2.8.

Camera Parent Lock
   When the camera is locked to the view and in fly mode, transform the parent rather than the camera.


Walk
----

Reverse Mouse
   Inverts the mouse's Y movement.
Mouse Sensitivity
   Speed factor for when looking around, high values mean faster mouse movement.
Teleport Duration
   Interval of time warp when teleporting in navigation mode.
Walk Speed
   Base speed for walking and flying.
Speed Factor
   The multiplication factor for the speed boost.


Gravity
-------

Simulates the effect of gravity when walking.

View Height
   The distance from the ground floor to the camera when walking
Jump Height
   The maximum height of a jump.
