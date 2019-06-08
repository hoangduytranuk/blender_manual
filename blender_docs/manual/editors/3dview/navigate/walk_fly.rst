.. _3dview-walk-fly:

*************
Walk/Fly Mode
*************

When you have to place the view, normally you do as described above.

However, there are cases in which you really prefer to just navigate your model,
especially if it is very large, like environments or some architectural model.
In these cases viewing the model in perspective mode has limitations,
for example after zooming a lot of panning is extremely uncomfortable and difficult,
or you apparently cannot move the camera any nearer. As an example,
try to navigate to a very distant object in the view with traditional methods
(explained above) and see what you can get.

With walk/fly modes you move, pan, tilt, and dolly the camera around without any of those limitations.

.. figure:: /images/editors_3dview_navigate_walk-fly_view-navigation-panel.png

   View Navigation.

In the :doc:`Preferences editor </editors/preferences/index>`
select the navigation mode you want to use as default when invoking the View Navigation operator.
Alternatively you can call the individual modes from the View Navigation menu.

.. note::

   This mode actually *moves* the camera used by the view.
   This means that when you are in camera view,
   it moves the active camera, which is another way to place and aim it.


.. _bpy.types.WalkNavigation:

Walk Mode
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> View Navigation --> Walk Navigation`
   :Hotkey:    :kbd:`Shift-F`

On activation the mouse pointer will move at the center of the view,
and a cross marker will appear...

This navigation mode behaves similar to the first person navigation system available in most 3D world games nowadays.
It works with a combination of keyboard keys :kbd:`W`, :kbd:`A`, :kbd:`S`, :kbd:`D` and mouse movement.
By default the navigation is in the "free" mode, with no gravity influence.
You can toggle between gravity and free mode during the navigation :kbd:`Tab`.

To move to places more quickly you can teleport :kbd:`Spacebar` around your scene.
If there is an object in front of the walk cross/aim you will move in that direction until you reach the point
(offset by the *camera height* value set in the :doc:`Preferences </editors/preferences/index>`).


Shortcuts
---------

- Move the mouse left/right to pan the view left/right or move it up/down to tilt the view up/down.
- Move the camera forward/backward :kbd:`W`, :kbd:`S`.
- Strafe left/right :kbd:`A`, :kbd:`D`.
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
   :Menu:      :menuselection:`View --> View Navigation --> Fly Navigation`
   :Hotkey:    :kbd:`Shift-F`

On activation the mouse pointer will move at the center of the view,
and a squared marker will appear -- a sort of HUD...

Some of the options of Fly mode are influenced by the position of
the mouse pointer relative to the center of the view itself,
and the squared marker around this center provides a sort of
"safe region" where you can place the mouse for it to have no effect on the view.
The more you take the mouse pointer away from the marker, the more you pan, or track, etc.


Shortcuts
---------

- Move the mouse left/right to pan the view left/right or move it up/down to tilt the view up/down.
- Move the view forward/backward:
  - :kbd:`WheelUp` or :kbd:`NumpadPlus` to accelerate the movement forward.
  - :kbd:`WheelDown` or :kbd:`NumpadMinus` to accelerate the movement backward.

    So if the view is already moving forward,
    :kbd:`WheelDown`, :kbd:`NumpadMinus` will eventually stop it and then move it backward, etc.
- Drag the :kbd:`MMB` to dolly.
  In this case the view can move laterally on its local axis at the moment you drag the mouse -- quite obviously,
  dragging left/right/up/down makes the view dolly on the left/right/up/down respectively.

When you are happy with the new view, click :kbd:`LMB` to confirm.
In case you want to go back from where you started, press :kbd:`Esc` or :kbd:`RMB`, as usual.
