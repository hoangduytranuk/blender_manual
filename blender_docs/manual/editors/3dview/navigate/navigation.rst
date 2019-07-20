
**********
Navigation
**********

Navigating in the 3D space is done with the use of both mouse movement and keyboard shortcuts.

To be able to work in the three-dimensional space that Blender uses,
you must be able to change your viewpoint as well as the viewing direction of the scene.
While we will describe the *3D View* editor, most of the other editors have similar functions.
For example, it is possible to pan and zoom in the Image editor.

.. tip:: Mouse Buttons and Numpad

   If you have a mouse with less than three buttons or a keyboard without a numpad,
   see the :doc:`Keyboard and Mouse </getting_started/configuration/hardware>`
   page of the manual to learn how to use them with Blender.


Navigation Gizmo
================

The navigation gizmo can be found in the top right of the editor.
The four buttons (listed from left to right) do the following:

- :doc:`Toggles the Projection </editors/3dview/navigate/projections>`
- :doc:`Toggles the Camera View </editors/3dview/navigate/camera_view>`
- `Pans the 3D Viewport <Panning>`_
- `Zooms the 3D Viewport <Zooming>`_

The `Orbit`_ gizmo on the far right can be used to rotate around 3D Viewport.
Hovering over the gizmo and dragging with :kbd:`LMB` will orbit the view.
Clicking any of the axis labels will :doc:`Align </editors/3dview/navigate/align>` to that view.
Clicking the same axis again switches to the opposite side of that same axis,

.. figure:: /images/editors_3dview_navigation_gizmo.png
   :align: center

   Navigation Gizmo.

Orbit
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Navigation --> Orbit`
   :Hotkey:    :kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`,
               :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`

Rotate the view around the point of interest.
Click and drag :kbd:`MMB` on the viewport's area.
If you start in the middle of the area and move up and down or left and right,
the view is rotated around the middle of the area.

To change the viewing angle in discrete steps, use :kbd:`Numpad8` and :kbd:`Numpad2`
or use :kbd:`Numpad4` and :kbd:`Numpad6`
to rotate the scene around the global Z axis from your current point of view.
Finally :kbd:`Numpad9` switches to the opposite side of the view.

Alternatively, if the *Emulate 3 button mouse* option is select in the *Preferences*
you can press and hold :kbd:`Alt` while dragging :kbd:`RMB` in the viewport's area.

.. note:: Hotkeys

   Remember that most hotkeys affect the **active** area (the one that has focus),
   so check that the mouse cursor is in the area you want to work in before you use the hotkeys.

.. seealso::

   - :ref:`Orbit Style Preference <prefs-input-orbit-style>`
   - :ref:`Auto-Perspective Preference <prefs-interface-auto-perspective>`


Roll
====

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Navigation --> Roll`
   :Hotkey:    :kbd:`Shift-Numpad4`, :kbd:`Shift-Numpad6`

Rotate the viewport camera around its local Z axis in 15° discrete steps.


Panning
=======

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Navigation --> Pan`
   :Hotkey:    :kbd:`Shift-MMB`, :kbd:`Ctrl-Numpad2`, :kbd:`Ctrl-Numpad4`,
               :kbd:`Ctrl-Numpad6`, :kbd:`Ctrl-Numpad8`

Moves the view up, down, left and right.
To pan the view, hold down :kbd:`Shift` and drag :kbd:`MMB` in the 3D View.
For discrete steps, use the hotkeys :kbd:`Ctrl-Numpad8`, :kbd:`Ctrl-Numpad2`,
:kbd:`Ctrl-Numpad4` and :kbd:`Ctrl-Numpad6` as with orbiting
(note: you can replace :kbd:`Ctrl` by :kbd:`Shift`).

For those without a middle mouse button,
you can hold :kbd:`Shift-Alt` while dragging with :kbd:`LMB`.


.. _editors_3dview_navigation_zoom:

Zooming
=======

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Navigation --> Zoom`
   :Hotkey:    :kbd:`Ctrl-MMB`, :kbd:`Wheel`, :kbd:`NumpadPlus`, :kbd:`NumpadMinus`

Moves the camera forwards and backwards.
You can zoom in and out by holding down :kbd:`Ctrl` and dragging :kbd:`MMB`.
The hotkeys are :kbd:`NumpadPlus` and :kbd:`NumpadMinus`.
The :menuselection:`View --> Navigation` submenu holds these functions too as well.
Refer to the 3D View's *View* menu image above for more information.
If you have a wheel mouse, you can zoom by rotating the :kbd:`Wheel`.

.. hint:: If You Get Lost

   If you get lost in 3D space, which is not uncommon, two hotkeys will help you:
   :kbd:`Home` changes the view so that you can see all objects :menuselection:`View --> Frame All`,
   while :kbd:`NumpadPeriod` zooms the view to the currently selected objects
   when in perspective mode :menuselection:`View --> Frame Selected`.


.. _3dview-nav-zoom-region:

Zoom Region
-----------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Navigation --> Zoom Region...`
   :Hotkey:    :kbd:`Shift-B`

The *Zoom Region* tool allows you to specify a rectangular region and zoom in
so that the region fills the 3D View.

You can access this through via the shortcut :kbd:`Shift-B`,
then :kbd:`LMB` click and drag a rectangle to zoom into.

Alternatively you can zoom out using the :kbd:`MMB`.


.. _3dview-nav-zoom-dolly:

Dolly Zoom
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Hotkey:    :kbd:`Shift-Ctrl-MMB`

In most cases its sufficient to zoom the view to get a closer look at something,
however, you may notice that at a certain point you cannot zoom any closer.

This is because Blender stores a view-point that is used for orbiting and zooming.
It works well in many cases, but sometimes you want to move the view-point to a different place.
This is what Dolly supports, allowing you to transport the view from one place to another.

You can dolly back and forth by holding down :kbd:`Shift-Ctrl` and dragging with :kbd:`MMB`.
