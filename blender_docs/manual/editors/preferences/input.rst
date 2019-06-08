.. _bpy.types.UserPreferencesInput:

*****
Input
*****

In the Input preferences, you can customize how Blender reacts to the mouse and keyboard as
well as define your own keymap.

.. figure:: /images/preferences_input_tab.png


Keyboard
========

Emulate Numpad
   The Numpad keys are used quite often in Blender and are not assigned to the same action as
   the regular number keys. If you have a keyboard without a Numpad (e.g. on a laptop),
   you can tell Blender to treat the standard number keys as Numpad keys by checking *Emulate Numpad*.
Default to Advanced Numeric Input
   TODO 2.8.


Mouse
=====

Emulate 3 Button Mouse
   Blender can be configured to work with pointing devices which do not have an :kbd:`MMB`
   (such as a two-button mouse, Apple's single-button mouse, or laptop touch-pad).
   The functionality of the three mouse buttons will then be emulated with
   key/mouse button combinations as shown in the table below.

   .. list-table:: Shortcuts for supported mouse hardware
      :header-rows: 1
      :class: valign
      :widths: 25 25 50

      * - 3-button Mouse
        - 2-button Mouse
        - Apple Mouse
      * - :kbd:`LMB`
        - :kbd:`LMB`
        - :kbd:`LMB` (mouse button)
      * - :kbd:`MMB`
        - :kbd:`Alt-LMB`
        - :kbd:`Alt-LMB` (Option/Alt key + mouse button)
      * - :kbd:`RMB`
        - :kbd:`RMB`
        - :kbd:`Cmd-LMB` (Command/Apple key + mouse button)

   Mouse/Keyboard combinations referenced in this manual
   can be expressed with the combinations shown in the table. For example:

   - :kbd:`MMB` drag becomes :kbd:`Alt-LMB` drag.
   - :kbd:`Shift-Alt-RMB` becomes :kbd:`Shift-Alt-Cmd-LMB` on a single-button mouse.

Continuous Grab
   This feature is used to prevent the problem where an action such as grabbing or panning a view,
   is limited by your screen bounds.

   This is done by warping the mouse within the view.

   .. note::

      Cursor warping is only supported by *relative* input devices (mouse, trackball, trackpad).

      Graphics tablets, however, typically use *absolute* positioning,
      this feature is disabled when a tablet is being used.

      This is detected for each action,
      so the presence of a tablet will not disable *Continuous Grab* for mouse cursor input.
Release Confirms
   Dragging :kbd:`LMB` on an object will move it.
   To confirm this (and other) transform, an :kbd:`LMB` is necessary by default.
   When this option is activated, the release of :kbd:`LMB` acts as confirmation of the transform.
Drag Threshold
   The number of pixels that a User Interface element has to be moved before it is recognized by Blender.
Motion Threshold
   The number of pixels the cursor must be moved before the movement is registered.
   This is helpful for tablet pens that are a lot more difficult to keep still
   then this could help to reduce stuttering of the cursor position.
Double Click Speed
   The time in ms for a double-click to be recognized.

.. note::

   The Mouse emulate option is only available if *Select With* is set to *Right*.


Tablet
======

Tablet API
   TODO 2.8.
Max Threshold
   Amount of pressure required to achieve full intensity.
Softness
   Controls how the softness of the low pressure response onset using a gamma curve.


NDOF
====

Pan Sensitivity
   The overall sensitivity for panning in the 3D View.
Orbit Sensitivity
   The overall sensitivity for orbiting in the 3D View.
Deadzone
   The threshold for the amount of movement needed from
   the device's rest position for Blender to interrupt that movement.

Navigate Method
   Navigation style for the viewport.

   Free
      Uses the full 6-degrees of freedom.
   Orbit
      Orbit about the view center.

Rotate Method
   Rotation style for the viewport.

   Turntable
      Rotates the view keeping the horizon horizontal.
   Trackball
      Is less restrictive, allowing any orientation.
