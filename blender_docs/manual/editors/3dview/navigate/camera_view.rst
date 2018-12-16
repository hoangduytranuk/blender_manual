
***********
Camera View
***********

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Camera`
   :Menu:      :menuselection:`View --> Camera --> Active Camera`
   :Hotkey:    :kbd:`Numpad0`

.. figure:: /images/editors_3dview_navigate_camera-view_example.png

   Demonstration of camera view.

The Camera view shows the current scene as seen from the currently active camera's view point.
It can be activated by pressing :kbd:`Numpad0`.
The Camera view can be used to virtually compose shots and preview how the scene will look when rendered.
The rendered image will contain everything within the dashed line.
In this view you can also set the *Render Border* which defines the portion of the 3D View to be rendered.

.. list-table:: Camera view provides a preview for the final rendered image.

   * - .. figure:: /images/editors_3dview_navigate_camera-view_preview.png
          :width: 335px

          Camera view.

     - .. figure:: /images/editors_3dview_navigate_camera-view_render.png
          :width: 335px

          Rendered image.


Camera Navigation
=================

There are several different ways to navigate and position the camera in your scene, some of them are explained below.

Zooming in and out is possible in this view, but to change the viewpoint,
you have to move or rotate the camera.

.. note::

   Remember that the active "camera" might be any kind of object.
   So these actions can be used, for example, to position and aim a lamp.


Move Active Camera to View
--------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Hotkey:    :kbd:`Ctrl-Alt-Numpad0`

This feature allows you to position and orient the active camera to match your current viewport.

Select a camera and then move around in the 3D View to a desired position and direction for
your camera (so that you are seeing what you want the camera to see). Now press
:kbd:`Ctrl-Alt-Numpad0` and your selected camera positions itself to match the view,
and switches to camera view.


Camera View Positioning
-----------------------

By enabling :ref:`Lock Camera to View <3dview-lock-camera-to-view>` in the View panel of the Properties region,
while in camera view, you can navigate the 3D View as usual,
while remaining in camera view. Controls are exactly the same as when normally moving in 3D.


Roll, Pan, Dolly, and Track
---------------------------

To perform these camera moves, the camera must first be *selected*,
so that it becomes the active object (while viewing through it,
you can :kbd:`RMB` -- click on the solid rectangular edges to select it).
The following actions also assume that you are in camera view :kbd:`Numpad0`!
Having done so, you can now manipulate the camera using the same tools
that are used to manipulate any object:

Roll
   Press :kbd:`R` to enter object rotation mode. The default will be to rotate the camera in its local Z axis
   (the axis orthogonal to the camera view), which is the definition of a camera "roll".
Vertical Pan or Pitch
   This is just a rotation along the local X axis. Press :kbd:`R` to enter object rotation mode, then :kbd:`X` twice
   (the first press selects the *global* axis, pressing the same letter a second time selects the *local* axis --
   this works with any axis;
   see the :doc:`axis locking page </editors/3dview/object/editing/transform/control/precision/axis_locking>`).
Horizontal Pan or Yaw
   This corresponds to a rotation around the camera's local Y axis.
   Press :kbd:`R`, and then :kbd:`Y` twice.
Dolly
   To dolly the camera, press :kbd:`G` then :kbd:`MMB` (or :kbd:`Z` twice).
Sideways Tracking
   Press :kbd:`G` and move the mouse (you can use :kbd:`X` twice or :kbd:`Y`
   to get pure-horizontal or pure-vertical sideways tracking).

.. seealso::

   :ref:`Fly/Walk Mode <3dview-walk-fly>`
      When you are in walk/fly mode, navigation actually moves your camera.
   :ref:`Lock Camera to View <3dview-lock-camera-to-view>`
      When enabled, performing typical view manipulation operations will move the camera object.
