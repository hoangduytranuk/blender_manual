.. _bpy.types.Area:
.. _bpy.types.AreaSpaces:

*****
Areas
*****

The application window is always a rectangle on your desktop.
It is divided up into a number of re-sizable areas.
An area contains the workspace for a particular type of editor,
like a 3D View Editor, or an Outliner.


Arranging
=========

Blender uses a novel screen-splitting approach to arrange areas.
The idea is that you split up that big application window into any number of smaller
(but still rectangular) non-overlapping areas. That way, each area is always fully visible,
and it is very easy to work in one area and hop over to work in another.


Changing the Size
-----------------

You can resize areas by dragging their borders with :kbd:`LMB`.
Simply move your mouse cursor over the border between two areas,
until it changes to a double-headed arrow, and then click and drag.


Splitting and Joining
---------------------

Area Split Widget
^^^^^^^^^^^^^^^^^

.. figure:: /images/interface_window-system_areas_split.png

In the upper right and lower left corners of an area are the area split widgets,
and they look like a little ridged thumb grip. It both splits and combines areas.
When you hover over it, your cursor will change to a cross (✛).

:kbd:`LMB` and drag it inward *split* the area.
You define the direction of that border by either dragging horizontally or vertically.

In order to *join* two areas :kbd:`LMB` click and drag the area splitter outward.
They must be the same dimension (width or height) in the direction you wish to join.
This is so that the combined area space results in a rectangle.

.. figure:: /images/interface_window-system_areas_join.png

   The Properties Editor is being merged "over" the Outliner.

The area that will be closed gets a dark overlaid with an arrow.
Now you can select the area to be closed by moving the mouse over it.

Release the :kbd:`LMB` to complete the join. If you press :kbd:`Esc`
or :kbd:`RMB` before releasing the mouse, the operation will be aborted.


Area Options
^^^^^^^^^^^^

:kbd:`RMB` on the border opens the *Area Options*.

Split Area
   Shows an indicator line that lets you select the area and position where to split.
   :kbd:`Tab` switches between vertical/horizontal.
Join Areas
   Shows the join direction overlay.

Confirm or cancel works as described above.


Swapping Contents
-----------------

You can swap the contents between two areas with :kbd:`Ctrl-LMB`
on one of the splitters of the initial area, dragging towards the target area,
and releasing the mouse there. The two areas do not need to be side-by-side,
though they must be inside the same window.


.. _bpy.ops.screen.area_dupli:

Duplicate Area into new Window
==============================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`View --> Duplicate Area into new Window`

The new window is a fully functional window, which is part of the same instance of Blender.
This can be useful, e.g. if you have multiple monitors.

A new window can be created from :menuselection:`View --> Duplicate Area into new Window`.

You can also create a new window from an existing area by :kbd:`Shift-LMB`
on the area splitter widget, then drag slightly.

The window can be closed with the OS *Close Window* button.


Toggle Maximize Area
====================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`View --> Toggle Maximize Area`
   :Hotkey:    :kbd:`Ctrl-Up`, :kbd:`Shift-Spacebar`

The maximized area fill the whole application window.
It contains the Info Editor and the select area.

You can maximize an area with the :menuselection:`View --> Toggle Maximize Area` menu entry.
To return to normal size use again menu entry, or :kbd:`RMB` on the editors header and
select *Maximize Area* and *Tiled Area* to return. In the Info Editor header
the *Back to Previous* button on the right of the menus also returns to tiled areas.

A quicker way to achieve this is to use the shortcuts: :kbd:`Shift-Spacebar`,
:kbd:`Ctrl-Down` or :kbd:`Ctrl-Up` to toggle between maximized and normal areas.

.. note::

   The area your mouse is currently hovering over is the one
   that will be maximized using the keyboard shortcuts.


.. _bpy.ops.screen.screen_full_area:

Toggle Fullscreen Area
======================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`View --> Toggle Fullscreen Area`
   :Hotkey:    :kbd:`Alt-F10`

The fullscreen area contains only the main region. The headers visibility can still
be toggled with the shortcut. To exit the fullscreen move the mouse to the top right corner
of the area to reveal the return icon or use the shortcut :kbd:`Alt-F10`.
