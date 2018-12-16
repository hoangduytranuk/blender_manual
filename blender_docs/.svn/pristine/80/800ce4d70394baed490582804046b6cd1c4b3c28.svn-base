.. _bpy.types.UserPreferencesInput:

*****
Input
*****

In the Input preferences, you can customize how Blender reacts to the mouse and keyboard as
well as define your own keymap.

.. figure:: /images/preferences_input_tab.png


Interaction
===========

Interaction Presets
   Presets that allow Blender to act like other software on your personal preference.


Mouse
-----

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

Drag Threshold
   The number of pixels that a User Interface element has to be moved before it is recognized by Blender.
Select With
   You can choose which button is used for selection (the other one is used to place the 3D cursor).
Double Click
   The time in ms for a double-click to be recognized.

.. note::

   The Mouse emulate option is only available if *Select With* is set to *Right*.


Emulate Numpad
--------------

The Numpad keys are used quite often in Blender and are not the same keys as the regular
number keys. If you have a keyboard without a Numpad (e.g. on a laptop),
you can tell Blender to treat the standard number keys as Numpad keys.
Just check *Emulate Numpad*.


View Manipulation
-----------------

.. _prefs-input-orbit-style:

Orbit Style
   Select how Blender works when you rotate the 3D View by default when holding :kbd:`MMB`.

   Turntable
      Rotates the view keeping the horizon horizontal.

      This behaves like a potter's wheel or record player where you have two axes of rotation available,
      and the world seems to have a better definition of what is "Up" and "Down" in it.

      The drawback to using the *Turntable* style is that you lose some flexibility when working with your objects.
      However, you gain the sense of "Up" and "Down" which can help if you are feeling disoriented.
   Trackball
      Is less restrictive, allowing any orientation.
Zoom Style
   Choose your preferred style of zooming in and out with :kbd:`Ctrl-MMB`.

   Scale
      *Scale* zooming depends on where you first click in the view.
      To zoom out, hold :kbd:`Ctrl-MMB` while dragging from the edge of the screen towards the center.
      To zoom in, hold :kbd:`Ctrl-MMB` while dragging from the center of the screen towards the edge.
   Continue
      The *Continue* zooming option allows you to control the speed
      (and not the value) of zooming by moving away from the initial click point with :kbd:`Ctrl-MMB`.
      Moving up from the initial click-point or to the right will zoom out,
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


View Navigation
---------------

Navigation Mode
   The default navigation mode for :kbd:`Shift-F` in the 3D View.


Walk Navigation
---------------

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
   Simulates the effect of gravity when walking.

   View Height
      The distance from the ground floor to the camera when walking.
   Jump Height
      The maximum height of a jump.


Fly
^^^

There are no additional options for fly mode.


NDOF Device
-----------

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


.. _prefs-input-keymap-editor:

Keymap Editor
=============

The Keymap editor lets you change the default Hotkeys. You can change keymaps for each of Blender's editors.

.. figure:: /images/preferences_input_keymap-editor.png

   Keymap editor.

Keymap Presets
   A list of predefined keymaps.

#. Select the keymap you want to change and click on the white arrows to open up the keymap tree.
#. Select which Input will control the function.

   - Keyboard: Only hotkey or combo hotkey :kbd:`E`, :kbd:`Shift-E`.
   - Mouse: Left/middle/right click. Can be combined with :kbd:`Alt`, :kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Cmd`.
   - NDOF: Movement from a :ref:`3D Mouse <hardware_3d-mice>`.
   - Tweak: Click and drag. Can also be combined with the four previous keys.
   - Text input: Use this function by entering a text.
   - Timer: Used to control actions based on a time period.
     e.g. By default, *Animation Step* uses "Timer 0", *Smooth View* uses "Timer 1".

#. Change hotkeys as you want. Just click on the shortcut input and enter the new shortcut.

If you want to restore the default settings for a keymap,
just click on the *Restore* button at the top right of this keymap.

.. tip::

   Instead of deleting the default keymap to create your custom one,
   you can just add a new *Preset* for both the mouse and keyboard.


Export/Import Key Configuration
===============================

In some cases, you may need to save your configuration in an external file
(e.g. if you need to install a new system or share your keymap configuration with the community).
To do this, simply press the *Export Key Configuration* button found in the header.
After doing so, the File Browser will open to choose where to store the configuration.
The *Import Key Configuration* button installs a keymap configuration that is on
your computer but not in Blender.

The exported keymap will only contain keymaps and categories that have been modified by the user.
In addition, add-ons may register keymaps to their respective functions,
however, these keymaps are not exported unless changed by the user.
This exported file may be thought of as a *"keymap delta"* instead of a full keymap export.
