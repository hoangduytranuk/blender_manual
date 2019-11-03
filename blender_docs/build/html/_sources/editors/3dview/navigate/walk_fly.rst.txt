.. _3dview-fly-walk:

*************
Fly/Walk Mode
*************

There are cases where it's preferable to navigate with first person controls,
especially for large environments such as architectural models.
In these cases orbiting around the view center is limiting.
While zoom, pan & dolly can be used, it's inconvenient.

With walk/fly modes you can navigate around the scene where view rotation is
performed from the cameras location.

.. figure:: /images/editors_3dview_navigate_walk-fly_view-navigation-panel.png

   View Navigation.

In the :doc:`Preferences editor </editors/preferences/index>`
select the navigation mode you want to use as default when invoking the View Navigation operator.
Alternatively you can call the individual modes from the View Navigation menu.

Common use cases for walk/fly include:

Navigation
   This can be a quick way to navigate a large scene.
Camera Placement
   When activated from a camera view, this will move the camera too.
Recording Animation
   Running from a camera with auto-keyframe and playing animation
   will record the motion as you make it allowing you to record the walk-through.


.. _bpy.types.WalkNavigation:

Walk Mode
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Hotkey:    :kbd:`Shift-AccentGrave`
   :Menu:      :menuselection:`View --> Navigation --> Walk Navigation`

On activation the mouse pointer will move at the center of the view,
and a cross marker will appear...

This navigation mode behaves similar to the first person navigation system available in most 3D world games.
It works with a combination of keyboard arrow keys and mouse movement.


Shortcuts
---------

- Move the mouse in the direction you want to look.
- Arrow keys or :kbd:`W`, :kbd:`A`, :kbd:`S`, :kbd:`D` move forwards/backwards and strafe left/right.
- Teleport :kbd:`Spacebar`.

  This moves you to the location at the cross-hair
  (offset by the *camera height* value set in the :doc:`Preferences </editors/preferences/index>`).
- Jump :kbd:`V` -- only in *gravity* mode.
- Move up and down :kbd:`Q`, :kbd:`E` -- only in *free* mode.
- Alternate between *free* and *gravity* modes :kbd:`Tab`.
- Change the movement speed:

  - :kbd:`WheelUp` or :kbd:`NumpadPlus` to increase the movement speed for this open session.
  - :kbd:`WheelDown` or :kbd:`NumpadMinus` to decrease the movement speed for this open session.
  - :kbd:`Shift` (hold) -- to speed up the movement temporarily.
  - :kbd:`Alt` (hold) -- to slow down the movement temporarily.

When you are happy with the new view, click :kbd:`LMB` to confirm.
In case you want to go back from where you started, press :kbd:`Esc` or :kbd:`RMB`, as usual.

If the defaults values (speed, mouse sensitivity, ...) need adjustments for your project,
in the :doc:`Preferences </editors/preferences/index>` you can select a few options for the navigation system:


Fly Mode
========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Hotkey:    :kbd:`Shift-AccentGrave`
   :Menu:      :menuselection:`View --> Navigation --> Fly Navigation`

On activation the cursor is centered inside a rectangle that defines a safe-region.
When the cursor is outside this region the view will rotate/pan.


Shortcuts
---------

- Move the mouse outside the safe-region in the direction you want to look.
- Move the view forward/backward:

  - :kbd:`WheelUp` or :kbd:`NumpadPlus` to accelerate the movement forward.
  - :kbd:`WheelDown` or :kbd:`NumpadMinus` to accelerate the movement backward.

    So if the view is already moving forward,
    :kbd:`WheelDown`, :kbd:`NumpadMinus` will eventually stop it and then move it backward, etc.
- :kbd:`MMB` Drag to pan the view.

  In this case the view can move laterally on its local axis at the moment you drag the mouse.
- :kbd:`Shift` precision (slow the momentum).
- :kbd:`Ctrl` disable rotation.

  While held, the view rotation doesn't influence the flight direction,
  this allows you to fly past an object, keeping it centered in the view,
  even as you fly away from it.

When you are happy with the new view, click :kbd:`LMB` to confirm.
In case you want to go back from where you started, press :kbd:`Esc` or :kbd:`RMB`, as usual.
